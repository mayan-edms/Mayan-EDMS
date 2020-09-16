import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    ConfirmView, SingleObjectDetailView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from ..events import event_document_view
from ..forms import DocumentFileDownloadForm, DocumentFilePreviewForm
from ..models import Document, DocumentFile
from ..permissions import (
    permission_document_file_revert, permission_document_file_view
)

from .document_views import DocumentDownloadFormView, DocumentDownloadView

__all__ = (
    'DocumentFileDownloadFormView', 'DocumentFileDownloadView',
    'DocumentFileListView', 'DocumentFileRevertView',
    'DocumentFileView'
)
logger = logging.getLogger(name=__name__)


class DocumentFileDownloadFormView(DocumentDownloadFormView):
    form_class = DocumentFileDownloadForm
    model = DocumentFile
    pk_url_kwarg = 'document_file_id'
    querystring_form_fields = (
        'compressed', 'zip_filename', 'preserve_extension'
    )
    viewname = 'documents:document_multiple_file_download'

    def get_extra_context(self):
        result = super(
            DocumentFileDownloadFormView, self
        ).get_extra_context()

        result.update({
            'title': _('Download document file'),
        })

        return result


class DocumentFileDownloadView(DocumentDownloadView):
    model = DocumentFile
    pk_url_kwarg = 'document_file_id'

    def get_item_filename(self, item):
        preserve_extension = self.request.GET.get(
            'preserve_extension', self.request.POST.get(
                'preserve_extension', False
            )
        )

        preserve_extension = preserve_extension == 'true' or preserve_extension == 'True'

        return item.get_rendered_string(preserve_extension=preserve_extension)


class DocumentFileListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_document_file_view
    external_object_pk_url_kwarg = 'document_id'

    def get_document(self):
        document = self.external_object
        document.add_as_recent_document_for_user(user=self.request.user)
        return document

    def get_extra_context(self):
        return {
            'hide_object': True,
            'list_as_items': True,
            'object': self.get_document(),
            'table_cell_container_classes': 'td-container-thumbnail',
            'title': _('Files of document: %s') % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().files.order_by('-timestamp')


class DocumentFileRevertView(ExternalObjectMixin, ConfirmView):
    external_object_class = DocumentFile
    external_object_permission = permission_document_file_revert
    external_object_pk_url_kwarg = 'document_file_id'

    def get_extra_context(self):
        return {
            'message': _(
                'All later file after this one will be deleted too.'
            ),
            'object': self.external_object.document,
            'title': _('Revert to this file?'),
        }

    def view_action(self):
        try:
            self.external_object.revert(_user=self.request.user)
            messages.success(
                message=_(
                    'Document file reverted successfully'
                ), request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error reverting document file; %s') % exception,
                request=self.request
            )


class DocumentFileView(SingleObjectDetailView):
    form_class = DocumentFilePreviewForm
    model = DocumentFile
    object_permission = permission_document_file_view
    pk_url_kwarg = 'document_file_id'

    def dispatch(self, request, *args, **kwargs):
        result = super(
            DocumentFileView, self
        ).dispatch(request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            request.user
        )
        event_document_view.commit(
            actor=request.user, target=self.object.document
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of document file: %s') % self.object,
        }
