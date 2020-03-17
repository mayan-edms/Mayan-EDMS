from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import ConfirmView
from mayan.apps.common.mixins import ExternalObjectMixin

from ..icons import icon_duplicated_document_list
from ..models import Document, DuplicatedDocument
from ..permissions import permission_document_tools, permission_document_view
from ..tasks import task_scan_duplicates_all

from .document_views import DocumentListView

__all__ = (
    'DocumentDuplicatesListView', 'DuplicatedDocumentListView',
    'ScanDuplicatedDocuments'
)
logger = logging.getLogger(name=__name__)


class DocumentDuplicatesListView(ExternalObjectMixin, DocumentListView):
    external_object_class = Document
    external_object_permission = permission_document_view
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        context = super(DocumentDuplicatesListView, self).get_extra_context()
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
        try:
            return DuplicatedDocument.objects.get(
                document=self.external_object
            ).documents.all()
        except DuplicatedDocument.DoesNotExist:
            return Document.objects.none()


class DuplicatedDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return DuplicatedDocument.objects.get_duplicated_documents()

    def get_extra_context(self):
        context = super(DuplicatedDocumentListView, self).get_extra_context()
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
        task_scan_duplicates_all.apply_async()
        messages.success(
            message=_('Duplicated document scan queued successfully.'),
            request=self.request
        )
