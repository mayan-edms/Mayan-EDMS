import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    ConfirmView, MultiFormView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.menus import menu_facet
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.common.models import SharedUploadedFile
from mayan.apps.documents.models import DocumentType, Document
from mayan.apps.documents.permissions import (
    permission_document_create, permission_document_new_version
)
from mayan.apps.documents.tasks import task_upload_new_version
from mayan.apps.navigation.classes import Link

from .exceptions import SourceException
from .forms import (
    NewDocumentForm, NewVersionForm, WebFormUploadForm, WebFormUploadFormHTML5
)
from .icons import (
    icon_log, icon_setup_sources, icon_staging_folder_file,
    icon_upload_view_link
)
from .literals import SOURCE_UNCOMPRESS_CHOICE_ASK, SOURCE_UNCOMPRESS_CHOICE_Y
from .links import (
    link_setup_source_create_imap_email, link_setup_source_create_pop3_email,
    link_setup_source_create_staging_folder,
    link_setup_source_create_watch_folder, link_setup_source_create_webform,
    link_setup_source_create_sane_scanner
)
from .models import (
    InteractiveSource, Source, SaneScanner, StagingFolderSource
)
from .permissions import (
    permission_sources_setup_create, permission_sources_setup_delete,
    permission_sources_setup_edit, permission_sources_setup_view,
    permission_staging_file_delete
)
from .tasks import task_check_interval_source, task_source_handle_upload
from .utils import get_class, get_form_class, get_upload_form_class

logger = logging.getLogger(name=__name__)


class SourceLogListView(ExternalObjectMixin, SingleObjectListView):
    external_object_queryset = Source.objects.select_subclasses()
    external_object_permission = permission_sources_setup_view
    external_object_pk_url_kwarg = 'source_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_log,
            'no_results_text': _(
                'Any error produced during the usage of a source will be '
                'listed here to assist in debugging.'
            ),
            'no_results_title': _('No log entries available'),
            'object': self.external_object,
            'title': _('Log entries for source: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.logs.all()


class UploadBaseView(MultiFormView):
    template_name = 'appearance/generic_form.html'
    prefixes = {'source_form': 'source', 'document_form': 'document'}

    @staticmethod
    def get_tab_link_for_source(source, document=None):
        if document:
            view = 'sources:document_version_upload'
            args = ('"{}"'.format(document.pk), '"{}"'.format(source.pk),)
        else:
            view = 'sources:document_upload_interactive'
            args = ('"{}"'.format(source.pk),)

        return Link(
            args=args,
            icon_class=icon_upload_view_link,
            keep_query=True,
            remove_from_query=['page'],
            text=source.label,
            view=view,
        )

    @staticmethod
    def get_active_tab_links(document=None):
        return [
            UploadBaseView.get_tab_link_for_source(source, document)
            for source in InteractiveSource.objects.filter(enabled=True).select_subclasses()
        ]

    def dispatch(self, request, *args, **kwargs):
        if 'source_id' in kwargs:
            self.source = get_object_or_404(
                klass=Source.objects.filter(enabled=True).select_subclasses(),
                pk=kwargs['source_id']
            )
        else:
            self.source = InteractiveSource.objects.filter(
                enabled=True
            ).select_subclasses().first()

        if not InteractiveSource.objects.filter(enabled=True).exists():
            messages.error(
                message=_(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                ), request=request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(viewname='sources:setup_source_list')
            )

        return super(UploadBaseView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UploadBaseView, self).get_context_data(**kwargs)
        subtemplates_list = []

        context['source'] = self.source

        if isinstance(self.source, StagingFolderSource):
            try:
                staging_filelist = list(self.source.get_files())
            except Exception as exception:
                messages.error(message=exception, request=self.request)
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
                            'no_results_icon': icon_staging_folder_file,
                            'no_results_text': _(
                                'This could mean that the staging folder is '
                                'empty. It could also mean that the '
                                'operating system user account being used '
                                'for Mayan EDMS doesn\'t have the necessary '
                                'file system permissions for the folder.'
                            ),
                            'no_results_title': _(
                                'No staging files available'
                            ),
                            'object_list': staging_filelist,
                            'title': _('Files in staging path'),
                        }
                    },
                ]
        elif isinstance(self.source, SaneScanner):
            subtemplates_list.append({
                'name': 'sources/upload_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                    'is_multipart': True,
                    'title': _('Document properties'),
                    'submit_label': _('Scan'),
                },
            })
        else:
            subtemplates_list.append({
                'name': 'sources/upload_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                    'is_multipart': True,
                    'title': _('Document properties'),
                },
            })

        menu_facet.bound_links['sources:document_upload_interactive'] = self.tab_links
        menu_facet.bound_links['sources:document_version_upload'] = self.tab_links

        context.update(
            {
                'subtemplates_list': subtemplates_list,
            }
        )

        return context


class UploadInteractiveView(UploadBaseView):
    def dispatch(self, request, *args, **kwargs):
        self.subtemplates_list = []

        self.document_type = get_object_or_404(
            klass=DocumentType, pk=self.request.GET.get(
                'document_type_id', self.request.POST.get('document_type_id')
            )
        )

        AccessControlList.objects.check_access(
            obj=self.document_type, permissions=(permission_document_create,),
            user=request.user
        )

        self.tab_links = UploadBaseView.get_active_tab_links()

        try:
            return super(
                UploadInteractiveView, self
            ).dispatch(request, *args, **kwargs)
        except Exception as exception:
            if request.is_ajax():
                return JsonResponse(
                    data={'error': force_text(exception)}, status=500
                )
            else:
                raise

    def forms_valid(self, forms):
        if self.source.can_compress:
            if self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                expand = forms['source_form'].cleaned_data.get('expand')
            else:
                if self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                    expand = True
                else:
                    expand = False
        else:
            expand = False

        try:
            uploaded_file = self.source.get_upload_file_object(
                forms['source_form'].cleaned_data
            )
        except SourceException as exception:
            messages.error(message=exception, request=self.request)
        else:
            shared_uploaded_file = SharedUploadedFile.objects.create(
                file=uploaded_file.file
            )

            if not self.request.user.is_anonymous:
                user_id = self.request.user.pk
            else:
                user_id = None

            try:
                self.source.clean_up_upload_file(uploaded_file)
            except Exception as exception:
                messages.error(message=exception, request=self.request)

            querystring = self.request.GET.copy()
            querystring.update(self.request.POST)

            try:
                task_source_handle_upload.apply_async(
                    kwargs=dict(
                        description=forms['document_form'].cleaned_data.get('description'),
                        document_type_id=self.document_type.pk,
                        expand=expand,
                        label=forms['document_form'].get_final_label(
                            filename=force_text(shared_uploaded_file)
                        ),
                        language=forms['document_form'].cleaned_data.get('language'),
                        querystring=querystring.urlencode(),
                        shared_uploaded_file_id=shared_uploaded_file.pk,
                        source_id=self.source.pk,
                        user_id=user_id,
                    )
                )
            except Exception as exception:
                message = _(
                    'Error executing document upload task; '
                    '%(exception)s'
                ) % {
                    'exception': exception,
                }
                logger.critical(msg=message, exc_info=True)
                raise type(exception)(message)
            else:
                messages.success(
                    message=_(
                        'New document queued for upload and will be available '
                        'shortly.'
                    ), request=self.request
                )

        return HttpResponseRedirect(
            redirect_to='{}?{}'.format(
                reverse(
                    viewname=self.request.resolver_match.view_name,
                    kwargs=self.request.resolver_match.kwargs
                ), self.request.META['QUERY_STRING']
            ),
        )

    def create_source_form_form(self, **kwargs):
        if hasattr(self.source, 'uncompress'):
            show_expand = self.source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK
        else:
            show_expand = False

        return self.get_form_classes()['source_form'](
            prefix=kwargs['prefix'],
            source=self.source,
            show_expand=show_expand,
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
        source_form_class = get_upload_form_class(
            source_type_name=self.source.source_type
        )

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
            'Upload a document of type "%(document_type)s" from '
            'source: %(source)s'
        ) % {'document_type': self.document_type, 'source': self.source.label}

        if not isinstance(self.source, StagingFolderSource) and not isinstance(self.source, SaneScanner):
            context['subtemplates_list'][0]['context'].update(
                {
                    'form_action': '{}?{}'.format(
                        reverse(
                            viewname=self.request.resolver_match.view_name,
                            kwargs=self.request.resolver_match.kwargs
                        ), self.request.META['QUERY_STRING']
                    ),
                    'form_css_classes': 'dropzone',
                    'form_disable_submit': True,
                    'form_id': 'html5upload',
                }
            )
        return context


class DocumentVersionUploadInteractiveView(UploadBaseView):
    def dispatch(self, request, *args, **kwargs):
        self.subtemplates_list = []

        self.document = get_object_or_404(
            klass=Document, pk=kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_new_version,),
            user=self.request.user
        )

        try:
            self.document.latest_version.execute_pre_save_hooks()
        except Exception as exception:
            messages.error(
                message=_(
                    'Unable to upload new versions for document '
                    '"%(document)s". %(exception)s'
                ) % {'document': self.document, 'exception': exception},
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='documents:document_version_list',
                    kwargs={'document_id': self.document.pk}
                )
            )

        self.tab_links = UploadBaseView.get_active_tab_links(self.document)

        return super(
            DocumentVersionUploadInteractiveView, self
        ).dispatch(request, *args, **kwargs)

    def forms_valid(self, forms):
        try:
            uploaded_file = self.source.get_upload_file_object(
                forms['source_form'].cleaned_data
            )
        except SourceException as exception:
            messages.error(message=exception, request=self.request)
        else:
            shared_uploaded_file = SharedUploadedFile.objects.create(
                file=uploaded_file.file
            )

            try:
                self.source.clean_up_upload_file(uploaded_file)
            except Exception as exception:
                messages.error(message=exception, request=self.request)

            if not self.request.user.is_anonymous:
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
                message=_(
                    'New document version queued for upload and will be '
                    'available shortly.'
                ), request=self.request
            )

        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='documents:document_version_list', kwargs={
                    'document_id': self.document.pk
                }
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

    def get_form_classes(self):
        source_form_class = get_upload_form_class(
            source_type_name=self.source.source_type
        )

        # Override source form class to enable the HTML5 file uploader
        if source_form_class == WebFormUploadForm:
            source_form_class = WebFormUploadFormHTML5

        return {
            'document_form': NewVersionForm,
            'source_form': source_form_class
        }

    def get_context_data(self, **kwargs):
        context = super(
            DocumentVersionUploadInteractiveView, self
        ).get_context_data(**kwargs)
        context['object'] = self.document
        context['title'] = _(
            'Upload a new version for document "%(document)s" '
            'from source: %(source)s'
        ) % {'document': self.document, 'source': self.source.label}
        context['submit_label'] = _('Submit')
        context['form_css_classes'] = 'dropzone'
        context['form_disable_submit'] = True
        context['form_action'] = '{}?{}'.format(
            reverse(
                viewname=self.request.resolver_match.view_name,
                kwargs=self.request.resolver_match.kwargs
            ), self.request.META['QUERY_STRING']
        )

        return context


class StagingFileDeleteView(ExternalObjectMixin, SingleObjectDeleteView):
    external_object_class = StagingFolderSource
    external_object_permission = permission_staging_file_delete
    external_object_pk_url_kwarg = 'staging_folder_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'object_name': _('Staging file'),
            'title': _('Delete staging file "%s"?') % self.object,
        }

    def get_object(self):
        return self.external_object.get_file(
            encoded_filename=self.kwargs['encoded_filename']
        )


# Setup views
class SetupSourceCheckView(ExternalObjectMixin, ConfirmView):
    """
    Trigger the task_check_interval_source task for a given source to
    test/debug their configuration irrespective of the schedule task setup.
    """
    external_object_pk_url_kwarg = 'source_id'
    external_object_queryset = Source.objects.select_subclasses()
    external_object_permission = permission_sources_setup_create

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'subtitle': _(
                'This will execute the source check code even if the source '
                'is not enabled. Sources that delete content after '
                'downloading will not do so while being tested. Check the '
                'source\'s error log for information during testing. A '
                'successful test will clear the error log.'
            ), 'title': _(
                'Trigger check for source "%s"?'
            ) % self.external_object,
        }

    def view_action(self):
        task_check_interval_source.apply_async(
            kwargs={
                'source_id': self.external_object.pk, 'test': True
            }
        )

        messages.success(
            message=_('Source check queued.'), request=self.request
        )


class SetupSourceCreateView(SingleObjectCreateView):
    post_action_redirect = reverse_lazy(
        viewname='sources:setup_source_list'
    )
    view_permission = permission_sources_setup_create

    def get_form_class(self):
        return get_form_class(
            source_type_name=self.kwargs['source_type_name']
        )

    def get_extra_context(self):
        return {
            'object': self.kwargs['source_type_name'],
            'title': _(
                'Create new source of type: %s'
            ) % get_class(
                source_type_name=self.kwargs['source_type_name']
            ).class_fullname(),
        }


class SetupSourceDeleteView(ExternalObjectMixin, SingleObjectDeleteView):
    external_object_queryset = Source.objects.select_subclasses()
    external_object_permission = permission_sources_setup_delete
    external_object_pk_url_kwarg = 'source_id'
    post_action_redirect = reverse_lazy(
        viewname='sources:setup_source_list'
    )

    def get_form_class(self):
        return get_form_class(source_type_name=self.get_object().source_type)

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the source: %s?') % self.get_object(),
        }

    def get_object(self):
        return self.external_object


class SetupSourceEditView(ExternalObjectMixin, SingleObjectEditView):
    external_object_queryset = Source.objects.select_subclasses()
    external_object_permission = permission_sources_setup_edit
    external_object_pk_url_kwarg = 'source_id'
    post_action_redirect = reverse_lazy(
        viewname='sources:setup_source_list'
    )
    view_permission = permission_sources_setup_edit

    def get_form_class(self):
        return get_form_class(source_type_name=self.get_object().source_type)

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit source: %s') % self.get_object(),
        }

    def get_object(self):
        return self.external_object


class SetupSourceListView(SingleObjectListView):
    object_permission = permission_sources_setup_view
    source_queryset = Source.objects.select_subclasses()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_setup_sources,
            'no_results_secondary_links': [
                link_setup_source_create_webform.resolve(
                    context=RequestContext(request=self.request)
                ),
                link_setup_source_create_imap_email.resolve(
                    context=RequestContext(request=self.request)
                ),
                link_setup_source_create_pop3_email.resolve(
                    context=RequestContext(request=self.request)
                ),
                link_setup_source_create_sane_scanner.resolve(
                    context=RequestContext(request=self.request)
                ),
                link_setup_source_create_staging_folder.resolve(
                    context=RequestContext(request=self.request)
                ),
                link_setup_source_create_watch_folder.resolve(
                    context=RequestContext(request=self.request)
                ),
            ],
            'no_results_text': _(
                'Sources provide the means to upload documents. '
                'Some sources like the webform, are interactive and require '
                'user input to operate. Others like the email sources, are '
                'automatic and run on the background without user intervention.'
            ),
            'no_results_title': _('No sources available'),
            'title': _('Sources'),
        }
