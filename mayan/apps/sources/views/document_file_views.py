import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.literals import DOCUMENT_FILE_ACTION_PAGES_NEW
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.documents.permissions import permission_document_file_new
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..forms import NewDocumentFileForm
from ..models import Source

from .base import UploadBaseView

__all__ = ('DocumentFileUploadInteractiveView',)
logger = logging.getLogger(name=__name__)


class DocumentFileUploadInteractiveView(
    ExternalObjectViewMixin, UploadBaseView
):
    document_form = NewDocumentFileForm
    external_object_queryset = Document.valid.all()
    external_object_permission = permission_document_file_new
    external_object_pk_url_kwarg = 'document_id'
    object_permission = permission_document_file_new

    def dispatch(self, request, *args, **kwargs):
        self.subtemplates_list = []

        result = super().dispatch(request, *args, **kwargs)

        try:
            DocumentFile.execute_pre_create_hooks(
                kwargs={
                    'document': self.external_object,
                    'file_object': None,
                    'user': self.request.user
                }
            )
        except Exception as exception:
            messages.error(
                message=_(
                    'Unable to upload new files for document '
                    '"%(document)s". %(exception)s'
                ) % {'document': self.external_object, 'exception': exception},
                request=self.request
            )
            return HttpResponseRedirect(
                redirect_to=reverse(
                    viewname='documents:document_file_list',
                    kwargs={'document_id': self.external_object.pk}
                )
            )

        return result

    def forms_valid(self, forms):
        source_backend_instance = self.source.get_backend_instance()

        try:
            source_backend_instance.process_document_file(
                document=self.external_object, forms=forms,
                request=self.request
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
                messages.error(
                    message=message.replace('\n', ' '),
                    request=self.request
                )
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
                    'document_id': self.external_object.pk
                }
            )
        )

    def get_active_tab_links(self):
        return [
            UploadBaseView.get_tab_link_for_source(
                source=source, document=self.external_object
            )
            for source in Source.objects.interactive().filter(enabled=True)
        ]

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
                'object': self.external_object,
                'title': _(
                    'Upload a new file for document "%(document)s" '
                    'from source: %(source)s'
                ) % {
                    'document': self.external_object,
                    'source': self.source.label
                },
                'submit_label': _('Submit')
            }
        )
        context.update(
            self.source.get_backend_instance().get_view_context(
                context=context, request=self.request
            )
        )

        return context

    def get_form_extra_kwargs__source_form(self, **kwargs):
        return {
            'source': self.source,
        }

    def get_initial__document_form(self):
        return {'action': DOCUMENT_FILE_ACTION_PAGES_NEW}
