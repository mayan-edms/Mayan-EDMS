import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import (
    permission_document_tools, permission_document_view
)
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import ConfirmView, SingleObjectListView
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .icons import icon_duplicated_document_list
from .models import DocumentStoredDuplicateBackend, StoredDuplicateBackend
from .tasks import task_duplicates_scan_all

logger = logging.getLogger(name=__name__)


class DocumentDuplicateBackendListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_pk_url_kwarg = 'document_id'
    external_object_permission = permission_document_view
    external_object_queryset = Document.valid.all()
    model = DocumentStoredDuplicateBackend

    def get_extra_context(self):
        return {
            'hide_object': True,
            'document': self.external_object,
            'object': self.external_object,
            'title': _(
                'Duplication criteria for document: %s'
            ) % self.external_object,
        }


class DocumentDuplicateBackendDetailView(ExternalObjectViewMixin, DocumentListView):
    external_object_permission = permission_document_view
    external_object_queryset = Document.valid.all()
    external_object_pk_url_kwarg = 'document_id'

    def dispatch(self, request, *args, **kwargs):
        self.stored_backend = self.get_stored_backend()
        result = super().dispatch(request, *args, **kwargs)
        return result

    def get_stored_backend(self):
        #TODO Add get_object_or_404
        return StoredDuplicateBackend.objects.get(pk=self.kwargs['backend_id'])

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'There are no documents that match the duplication '
                    'criteria.'
                ),
                'no_results_title': _(
                    'There are no duplicated document'
                ),
                'object': self.external_object,
                'stored_backend': self.stored_backend,
                'title': _(
                    'Duplicates for document "%s" using criteria: %s'
                ) % (self.external_object, self.stored_backend)
            }
        )
        return context

    def get_source_queryset(self):
        return self.stored_backend.get_duplicated_documents(
            source_document=self.external_object
        )


class DuplicateBackendListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Duplication criteria'),
    }
    model = StoredDuplicateBackend


class DuplicateBackendDetailView(ExternalObjectViewMixin, DocumentListView):
    external_object_class = StoredDuplicateBackend
    external_object_pk_url_kwarg = 'backend_id'

    def get_document_queryset(self):
        return self.external_object.get_duplicated_documents()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'Duplicates are documents share some common attribute. '
                    'The exact attribute that will be matched will change '
                    'based on the criteria algorithm.'
                ),
                'no_results_title': _(
                    'There are no duplicated documents'
                ),
                'stored_backend': self.external_object,
                'title': _(
                    'Duplicated documents by criteria: %s'
                ) % self.external_object
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
