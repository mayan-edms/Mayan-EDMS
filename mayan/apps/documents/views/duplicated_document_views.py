from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    FormView, MultipleObjectConfirmActionView, MultipleObjectFormActionView,
    SingleObjectDetailView, SingleObjectListView
)

from ..events import event_document_view
from ..icons import icon_document_list, icon_duplicated_document_list
from ..models import Document, DuplicatedDocument
from ..permissions import permission_document_view

from .document_views import DocumentListView

__all__ = ('DocumentDuplicatesListView', 'DuplicatedDocumentListView')
logger = logging.getLogger(__name__)


class DocumentDuplicatesListView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document(), permissions=(permission_document_view,),
            user=self.request.user
        )

        return super(
            DocumentDuplicatesListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

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
                'object': self.get_document(),
                'title': _('Duplicates for document: %s') % self.get_document(),
            }
        )
        return context

    def get_source_queryset(self):
        try:
            return DuplicatedDocument.objects.get(
                document=self.get_document()
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
