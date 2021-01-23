import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.literals import DOCUMENT_FILE_ACTION_PAGES_NEW
from mayan.apps.documents.models import Document, DocumentFile
from mayan.apps.documents.permissions import permission_document_file_new
from mayan.apps.documents.tasks import task_document_file_upload
from mayan.apps.storage.models import SharedUploadedFile

from ..exceptions import SourceException
from ..forms import NewFileForm, WebFormUploadForm, WebFormUploadFormHTML5
from ..models import SaneScanner, StagingFolderSource
from ..utils import get_upload_form_class

from .document_views import UploadBaseView

__all__ = ('DocumentFileUploadInteractiveView',)
logger = logging.getLogger(name=__name__)


class DocumentFileUploadInteractiveView(UploadBaseView):
    def create_source_form_form(self, **kwargs):
        return self.get_form_classes()['source_form'](
            prefix=kwargs['prefix'],
            source=self.source,
            show_expand=False,
            data=kwargs.get('data', None),
            files=kwargs.get('files', None),
        )

    def dispatch(self, request, *args, **kwargs):
        self.subtemplates_list = []

        self.document = get_object_or_404(
            klass=Document.valid, pk=kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_file_new,),
            user=self.request.user
        )

        try:
            DocumentFile.execute_pre_create_hooks(
                kwargs={
                    'document': self.document,
                    'shared_uploaded_file': None,
                    'user': self.request.user
                }
            )
        except Exception as exception:
            messages.error(
                message=_(
                    'Unable to upload new files for document '
                    '"%(document)s". %(exception)s'
                ) % {'document': self.document, 'exception': exception},
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='documents:document_file_list',
                    kwargs={'document_id': self.document.pk}
                )
            )

        self.tab_links = UploadBaseView.get_active_tab_links(
            document=self.document
        )

        return super().dispatch(request, *args, **kwargs)

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
                user = self.request.user
                user_id = self.request.user.pk
            else:
                user = None
                user_id = None

            try:
                DocumentFile.execute_pre_create_hooks(
                    kwargs={
                        'document': self.document,
                        'shared_uploaded_file': shared_uploaded_file,
                        'user': user
                    }
                )

                task_document_file_upload.apply_async(
                    kwargs={
                        'action': int(
                            forms['document_form'].cleaned_data.get('action')
                        ),
                        'comment': forms['document_form'].cleaned_data.get('comment'),
                        'document_id': self.document.pk,
                        'shared_uploaded_file_id': shared_uploaded_file.pk,
                        'user_id': user_id
                    }
                )
            except Exception as exception:
                message = _(
                    'Error executing document file upload task; '
                    '%(exception)s'
                ) % {
                    'exception': exception,
                }
                logger.critical(msg=message, exc_info=True)
                if self.request.is_ajax():
                    return JsonResponse(
                        data={'error': force_text(s=message)}, status=500
                    )
                else:
                    raise type(exception)(message)
            else:
                messages.success(
                    message=_(
                        'New document file queued for upload and will be '
                        'available shortly.'
                    ), request=self.request
                )

        return HttpResponseRedirect(
            redirect_to=reverse(
                viewname='documents:document_file_list', kwargs={
                    'document_id': self.document.pk
                }
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'form_action': '{}?{}'.format(
                    reverse(
                        viewname=self.request.resolver_match.view_name,
                        kwargs=self.request.resolver_match.kwargs
                    ), self.request.META['QUERY_STRING']
                ),
                'object': self.document,
                'title': _(
                    'Upload a new file for document "%(document)s" '
                    'from source: %(source)s'
                ) % {'document': self.document, 'source': self.source.label},
                'submit_label': _('Submit')
            }
        )

        if not isinstance(self.source, StagingFolderSource) and not isinstance(self.source, SaneScanner):
            context.update(
                {
                    'form_css_classes': 'dropzone',
                    'form_disable_submit': True
                }
            )

        return context

    def get_document_form_initial(self):
        return {'action': DOCUMENT_FILE_ACTION_PAGES_NEW}

    def get_form_classes(self):
        source_form_class = get_upload_form_class(
            source_type_name=self.source.source_type
        )

        # Override source form class to enable the HTML5 file uploader
        if source_form_class == WebFormUploadForm:
            source_form_class = WebFormUploadFormHTML5

        return {
            'document_form': NewFileForm,
            'source_form': source_form_class
        }
