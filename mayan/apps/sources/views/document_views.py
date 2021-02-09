import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import (
    DocumentType, Document, DocumentFile
)
from mayan.apps.documents.permissions import permission_document_create
from mayan.apps.navigation.classes import Link
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.views.generics import MultiFormView

from ..exceptions import SourceException
from ..forms import (
    NewDocumentForm, WebFormUploadForm, WebFormUploadFormHTML5
)
from ..icons import icon_staging_folder_file, icon_upload_view_link
from ..literals import SOURCE_UNCOMPRESS_CHOICE_ASK, SOURCE_UNCOMPRESS_CHOICE_Y
from ..links import factory_conditional_active_by_source
from ..menus import menu_sources
from ..models import (
    InteractiveSource, Source, SaneScanner, StagingFolderSource
)
from ..tasks import task_source_handle_upload
from ..utils import get_upload_form_class

__all__ = ('UploadBaseView', 'UploadInteractiveView')
logger = logging.getLogger(name=__name__)


class UploadBaseView(MultiFormView):
    prefixes = {'source_form': 'source', 'document_form': 'document'}
    template_name = 'appearance/generic_form.html'

    @staticmethod
    def get_active_tab_links(document=None):
        return [
            UploadBaseView.get_tab_link_for_source(source, document)
            for source in InteractiveSource.objects.filter(enabled=True).select_subclasses()
        ]

    @staticmethod
    def get_tab_link_for_source(source, document=None):
        if document:
            view = 'sources:document_file_upload'
            args = ('"{}"'.format(document.pk), '"{}"'.format(source.pk),)
        else:
            view = 'sources:document_upload_interactive'
            args = ('"{}"'.format(source.pk),)

        return Link(
            args=args,
            conditional_active=factory_conditional_active_by_source(
                source=source
            ), icon=icon_upload_view_link, keep_query=True,
            remove_from_query=['page'], text=source.label, view=view
        )

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

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                'name': 'appearance/generic_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                    'is_multipart': True,
                    'title': _('Document properties'),
                    'submit_label': _('Scan'),
                },
            })
        else:
            subtemplates_list.append({
                'name': 'appearance/generic_multiform_subtemplate.html',
                'context': {
                    'forms': context['forms'],
                    'is_multipart': True,
                    'title': _('Document properties'),
                },
            })

        menu_sources.bound_links['sources:document_upload_interactive'] = self.tab_links
        menu_sources.bound_links['sources:document_file_upload'] = self.tab_links

        context.update(
            {
                'subtemplates_list': subtemplates_list,
            }
        )

        return context


class UploadInteractiveView(UploadBaseView):
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
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            if request.is_ajax():
                return JsonResponse(
                    data={'error': force_text(s=exception)}, status=500
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
                user = self.request.user
                user_id = self.request.user.pk
            else:
                user = None
                user_id = None

            try:
                self.source.clean_up_upload_file(uploaded_file)
            except Exception as exception:
                messages.error(message=exception, request=self.request)

            querystring = self.request.GET.copy()
            querystring.update(self.request.POST)

            try:
                Document.execute_pre_create_hooks(
                    kwargs={
                        'document_type': self.document_type,
                        'user': user
                    }
                )

                DocumentFile.execute_pre_create_hooks(
                    kwargs={
                        'document_type': self.document_type,
                        'shared_uploaded_file': shared_uploaded_file,
                        'user': user
                    }
                )

                task_source_handle_upload.apply_async(
                    kwargs={
                        'description': forms['document_form'].cleaned_data.get('description'),
                        'document_type_id': self.document_type.pk,
                        'expand': expand,
                        'label': forms['document_form'].get_final_label(
                            filename=force_text(s=shared_uploaded_file)
                        ),
                        'language': forms['document_form'].cleaned_data.get('language'),
                        'querystring': querystring.urlencode(),
                        'shared_uploaded_file_id': shared_uploaded_file.pk,
                        'source_id': self.source.pk,
                        'user_id': user_id,
                    }
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
