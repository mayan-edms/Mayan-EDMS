from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common import menu_facet
from common.models import SharedUploadedFile
from common.utils import encapsulate
from common.views import (
    MultiFormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from common.widgets import two_state_template
from documents.models import DocumentType, Document, NewVersionBlock
from documents.permissions import (
    permission_document_create, permission_document_new_version
)
from documents.tasks import task_upload_new_version
from metadata.api import decode_metadata_from_url
from navigation import Link
from organizations.models import Organization
from permissions import Permission

from .forms import (
    NewDocumentForm, NewVersionForm, WebFormUploadForm,
    WebFormUploadFormHTML5
)
from .literals import (
    SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WEB_FORM,
    SOURCE_UNCOMPRESS_CHOICE_ASK,
    SOURCE_UNCOMPRESS_CHOICE_Y
)
from .models import (
    InteractiveSource, Source, StagingFolderSource, WebFormSource
)
from .permissions import (
    permission_sources_setup_create, permission_sources_setup_delete,
    permission_sources_setup_edit, permission_sources_setup_view,
    permission_staging_file_delete
)
from .tasks import task_source_handle_upload
from .utils import get_class, get_form_class, get_upload_form_class


class SourceLogListView(SingleObjectListView):
    view_permission = permission_sources_setup_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.get_source(),
            'title': _('Log entries for source: %s') % self.get_source(),
        }

    def get_queryset(self):
        return self.get_source().logs.all()

    def get_source(self):
        return get_object_or_404(
            Source.on_organization.select_subclasses(), pk=self.kwargs['pk']
        )


class UploadBaseView(MultiFormView):
    template_name = 'appearance/generic_form.html'
    prefixes = {'source_form': 'source', 'document_form': 'document'}

    @staticmethod
    def get_tab_link_for_source(source, document=None):
        if document:
            view = 'sources:upload_version'
            args = ('"{}"'.format(document.pk), '"{}"'.format(source.pk),)
        else:
            view = 'sources:upload_interactive'
            args = ('"{}"'.format(source.pk),)

        return Link(
            text=source.label,
            view=view,
            args=args,
            keep_query=True,
            remove_from_query=['page'],
            icon='fa fa-upload',
        )

    @staticmethod
    def get_active_tab_links(document=None):
        tab_links = []

        web_forms = WebFormSource.on_organization.filter(enabled=True)
        for web_form in web_forms:
            tab_links.append(
                UploadBaseView.get_tab_link_for_source(web_form, document)
            )

        staging_folders = StagingFolderSource.on_organization.filter(enabled=True)
        for staging_folder in staging_folders:
            tab_links.append(
                UploadBaseView.get_tab_link_for_source(
                    staging_folder, document
                )
            )

        return {
            'tab_links': tab_links,
            SOURCE_CHOICE_WEB_FORM: web_forms,
            SOURCE_CHOICE_STAGING: staging_folders,
        }

    def dispatch(self, request, *args, **kwargs):
        if 'source_id' in kwargs:
            self.source = get_object_or_404(
                Source.on_organization.filter(enabled=True).select_subclasses(),
                pk=kwargs['source_id']
            )
        else:
            self.source = InteractiveSource.on_organization.filter(
                enabled=True
            ).select_subclasses().first()

        if not InteractiveSource.on_organization.filter(enabled=True).exists():
            messages.error(
                request,
                _(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                )
            )
            return HttpResponseRedirect(reverse('sources:setup_source_list'))

        return super(UploadBaseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadBaseView, self).get_context_data(**kwargs)
        subtemplates_list = []

        context['source'] = self.source

        if isinstance(self.source, StagingFolderSource):
            try:
                staging_filelist = list(self.source.get_files())
            except Exception as exception:
                messages.error(self.request, exception)
                staging_filelist = []
            finally:
                subtemplates_list = [
                    {
                        'name': 'appearance/generic_multiform_subtemplate.html',
                        'context': {
                            'forms': context['forms'],
                            'title': _('Document properties'),
                        }
                    },
                    {
                        'name': 'appearance/generic_list_subtemplate.html',
                        'context': {
                            'hide_link': True,
                            'object_list': staging_filelist,
                            'title': _('Files in staging path'),
                        }
                    },
                ]
        else:
            subtemplates_list.append({
                'name': 'sources/upload_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                    'is_multipart': True,
                    'title': _('Document properties'),
                },
            })

        menu_facet.bound_links['sources:upload_interactive'] = self.tab_links['tab_links']
        menu_facet.bound_links['sources:upload_version'] = self.tab_links['tab_links']

        context.update({
            'subtemplates_list': subtemplates_list,
        })

        return context


class UploadInteractiveView(UploadBaseView):
    def dispatch(self, request, *args, **kwargs):
        self.subtemplates_list = []

        self.document_type = get_object_or_404(
            DocumentType,
            pk=self.request.GET.get(
                'document_type_id', self.request.POST.get('document_type_id')
            )
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_create,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_create, request.user,
                self.document_type
            )

        self.tab_links = UploadBaseView.get_active_tab_links()

        return super(
            UploadInteractiveView, self
        ).dispatch(request, *args, **kwargs)

    def forms_valid(self, forms):
        if self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
            expand = forms['source_form'].cleaned_data.get('expand')
        else:
            if self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                expand = True
            else:
                expand = False

        uploaded_file = self.source.get_upload_file_object(
            forms['source_form'].cleaned_data
        )

        shared_uploaded_file = SharedUploadedFile.objects.create(
            file=uploaded_file.file
        )

        label = None

        if 'document_type_available_filenames' in forms['document_form'].cleaned_data:
            if forms['document_form'].cleaned_data['document_type_available_filenames']:
                label = forms['document_form'].cleaned_data['document_type_available_filenames'].filename

        if not self.request.user.is_anonymous():
            user_id = self.request.user.pk
        else:
            user_id = None

        try:
            self.source.clean_up_upload_file(uploaded_file)
        except Exception as exception:
            messages.error(self.request, exception)

        task_source_handle_upload.apply_async(kwargs=dict(
            description=forms['document_form'].cleaned_data.get('description'),
            document_type_id=self.document_type.pk,
            expand=expand,
            label=label,
            language=forms['document_form'].cleaned_data.get('language'),
            metadata_dict_list=decode_metadata_from_url(self.request.GET),
            shared_uploaded_file_id=shared_uploaded_file.pk,
            source_id=self.source.pk,
            tag_ids=self.request.GET.getlist('tags'),
            user_id=user_id,
        ))
        messages.success(
            self.request,
            _(
                'New document queued for uploaded and will be available '
                'shortly.'
            )
        )
        return HttpResponseRedirect(self.request.get_full_path())

    def create_source_form_form(self, **kwargs):
        return self.get_form_classes()['source_form'](
            prefix=kwargs['prefix'],
            source=self.source,
            show_expand=(
                self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK
            ),
            data=kwargs.get('data', None),
            files=kwargs.get('files', None),
        )

    def create_document_form_form(self, **kwargs):
        return self.get_form_classes()['document_form'](
            prefix=kwargs['prefix'],
            document_type=self.document_type,
            data=kwargs.get('data', None),
            files=kwargs.get('files', None),
        )

    def get_form_classes(self):
        source_form_class = get_upload_form_class(self.source.source_type)

        # Override source form class to enable the HTML5 file uploader
        if source_form_class == WebFormUploadForm:
            source_form_class = WebFormUploadFormHTML5

        return {
            'document_form': NewDocumentForm,
            'source_form': source_form_class
        }

    def get_context_data(self, **kwargs):
        context = super(UploadInteractiveView, self).get_context_data(**kwargs)
        context['title'] = _(
            'Upload a local document from source: %s'
        ) % self.source.label
        if not isinstance(self.source, StagingFolderSource):
            context['subtemplates_list'][0]['context'].update(
                {
                    'form_action': self.request.get_full_path(),
                    'form_class': 'dropzone',
                    'form_disable_submit': True,
                    'form_id': 'html5upload',
                }
            )
        return context


class UploadInteractiveVersionView(UploadBaseView):
    def dispatch(self, request, *args, **kwargs):

        self.subtemplates_list = []

        self.document = get_object_or_404(Document, pk=kwargs['document_pk'])

        if NewVersionBlock.objects.is_blocked(self.document):
            messages.error(
                self.request,
                _(
                    'Document "%s" is blocked from uploading new versions.'
                ) % self.document
            )
            return HttpResponseRedirect(
                reverse(
                    'documents:document_version_list', args=(self.document.pk,)
                )
            )

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_new_version,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_new_version, self.request.user,
                self.document
            )

        self.tab_links = UploadBaseView.get_active_tab_links(self.document)

        return super(
            UploadInteractiveVersionView, self
        ).dispatch(request, *args, **kwargs)

    def forms_valid(self, forms):
        uploaded_file = self.source.get_upload_file_object(
            forms['source_form'].cleaned_data
        )

        shared_uploaded_file = SharedUploadedFile.objects.create(
            file=uploaded_file.file
        )

        try:
            self.source.clean_up_upload_file(uploaded_file)
        except Exception as exception:
            messages.error(self.request, exception)

        if not self.request.user.is_anonymous():
            user_id = self.request.user.pk
        else:
            user_id = None

        task_upload_new_version.apply_async(kwargs=dict(
            shared_uploaded_file_id=shared_uploaded_file.pk,
            document_id=self.document.pk,
            user_id=user_id,
            comment=forms['document_form'].cleaned_data.get('comment')
        ))

        messages.success(
            self.request,
            _(
                'New document version queued for uploaded and will be '
                'available shortly.'
            )
        )
        return HttpResponseRedirect(
            reverse(
                'documents:document_version_list', args=(self.document.pk,)
            )
        )

    def create_source_form_form(self, **kwargs):
        return self.get_form_classes()['source_form'](
            prefix=kwargs['prefix'],
            source=self.source,
            show_expand=False,
            data=kwargs.get('data', None),
            files=kwargs.get('files', None),
        )

    def create_document_form_form(self, **kwargs):
        return self.get_form_classes()['document_form'](
            prefix=kwargs['prefix'],
            data=kwargs.get('data', None),
            files=kwargs.get('files', None),
        )

    def get_form_classes(self):
        return {
            'document_form': NewVersionForm,
            'source_form': get_upload_form_class(self.source.source_type)
        }

    def get_context_data(self, **kwargs):
        context = super(
            UploadInteractiveVersionView, self
        ).get_context_data(**kwargs)
        context['object'] = self.document
        context['title'] = _(
            'Upload a new version from source: %s'
        ) % self.source.label

        return context


class StagingFileDeleteView(SingleObjectDeleteView):
    object_permission = permission_staging_file_delete
    object_permission_related = 'staging_folder'

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'object_name': _('Staging file'),
            'source': self.get_source(),
        }

    def get_object(self):
        source = self.get_source()
        return source.get_file(
            encoded_filename=self.kwargs['encoded_filename']
        )

    def get_source(self):
        return get_object_or_404(
            StagingFolderSource, pk=self.kwargs['pk']
        )


# Setup views
class SetupSourceCreateView(SingleObjectCreateView):
    post_action_redirect = reverse_lazy('sources:setup_source_list')
    view_permission = permission_sources_setup_create

    def get_extra_context(self):
        return {
            'object': self.kwargs['source_type'],
            'title': _(
                'Create new source of type: %s'
            ) % get_class(self.kwargs['source_type']).class_fullname(),
        }

    def get_form_class(self):
        return get_form_class(self.kwargs['source_type'])

    def get_instance_extra_data(self):
        return {'organization': Organization.objects.get_current()}


class SetupSourceDeleteView(SingleObjectDeleteView):
    post_action_redirect = reverse_lazy('sources:setup_source_list')
    view_permission = permission_sources_setup_delete

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the source: %s?') % self.get_object(),
        }

    def get_form_class(self):
        return get_form_class(self.get_object().source_type)

    def get_object(self):
        return get_object_or_404(
            Source.on_organization.select_subclasses(), pk=self.kwargs['pk']
        )


class SetupSourceEditView(SingleObjectEditView):
    post_action_redirect = reverse_lazy('sources:setup_source_list')
    view_permission = permission_sources_setup_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit source: %s') % self.get_object(),
        }

    def get_form_class(self):
        return get_form_class(self.get_object().source_type)

    def get_object(self):
        return get_object_or_404(
            Source.on_organization.select_subclasses(), pk=self.kwargs['pk']
        )


class SetupSourceListView(SingleObjectListView):
    queryset = Source.on_organization.select_subclasses()
    view_permission = permission_sources_setup_view

    extra_context = {
        'extra_columns': (
            {
                'name': _('Type'),
                'attribute': encapsulate(lambda entry: entry.class_fullname())
            },
            {
                'name': _('Enabled'),
                'attribute': encapsulate(
                    lambda entry: two_state_template(entry.enabled)
                )
            },
        ),
        'hide_link': True,
        'title': _('Sources'),
    }
