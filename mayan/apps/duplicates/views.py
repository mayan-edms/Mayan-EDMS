import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import (
    permission_document_tools, permission_document_view
)
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import ConfirmView
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .icons import icon_duplicated_document_list
from .models import DuplicateBackendEntry
from .tasks import task_duplicates_scan_all

logger = logging.getLogger(name=__name__)


class DocumentDuplicatesListView(ExternalObjectViewMixin, DocumentListView):
    external_object_permission = permission_document_view
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'Only exact copies of this document will be shown in the '
                    'this list.'
                ),
                'no_results_title': _(
                    'There are no duplicates for this document'
                ),
                'object': self.external_object,
                'title': _(
                    'Duplicates for document: %s'
                ) % self.external_object,
            }
        )
        return context

    def get_source_queryset(self):
        return DuplicateBackendEntry.objects.get_duplicates_of(
            document=self.external_object
        )


class DuplicatedDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return DuplicateBackendEntry.objects.get_duplicated_documents(
            permission=permission_document_view, user=self.request.user
        )

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'Duplicates are documents that are composed of the exact '
                    'same file, down to the last byte. Files that have the '
                    'same text or OCR but are not identical or were saved '
                    'using a different file format will not appear as '
                    'duplicates.'
                ),
                'no_results_title': _(
                    'There are no duplicated documents'
                ),
                'title': _('Duplicated documents')
            }
        )
        return context


class ScanDuplicatedDocuments(ConfirmView):
    extra_context = {
        'title': _('Scan for duplicated documents?')
    }
    view_permission = permission_document_tools

    def view_action(self):
        task_duplicates_scan_all.apply_async()
        messages.success(
            message=_('Duplicated document scan queued successfully.'),
            request=self.request
        )
