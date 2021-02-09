import logging

from django.apps import apps
from django.db import models
from django.db.models import Q, Value

from mayan.apps.acls.models import AccessControlList

from .classes import DuplicateBackend

logger = logging.getLogger(name=__name__)


class StoredDuplicateBackendManager(models.Manager):
    def scan_all(self):
        """
        Find duplicates by iterating over all documents and all backends.
        """
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        for document in Document.valid.all():
            self.scan_document(document=document, scan_children=False)

    def scan_document(self, document, scan_children=True):
        """
        Find duplicates by matching latest file checksums
        """
        if not document.file_latest:
            return None

        for backend_path, backend_class in DuplicateBackend.get_all():
            stored_backend, created = self.get_or_create(
                backend_path=backend_path
            )
            duplicates = stored_backend.get_backend_instance().process(document=document)

            if duplicates.exists():
                duplicates_entry, created = stored_backend.duplicate_entries.get_or_create(
                    document=document
                )
                duplicates_entry.documents.add(*duplicates)
            else:
                stored_backend.duplicate_entries.filter(document=document).delete()

            if scan_children:
                for document in duplicates:
                    self.scan_document(document=document, scan_children=False)


class DuplicateBackendEntryManager(models.Manager):
    def clean_empty_duplicate_lists(self):
        self.filter(documents=None).delete()

    def get_duplicated_documents(self, permission=None, user=None):
        DuplicateSourceDocument = apps.get_model(
            app_label='duplicates', model_name='DuplicateSourceDocument'
        )
        DuplicateTargetDocument = apps.get_model(
            app_label='duplicates', model_name='DuplicateTargetDocument'
        )

        target_document_queryset = DuplicateTargetDocument.valid.all()

        if permission:
            target_document_queryset = AccessControlList.objects.restrict_queryset(
                queryset=target_document_queryset, permission=permission,
                user=user
            )

        queryset = self.filter(documents__in=target_document_queryset).only(
            'document_id'
        ).values('document_id')

        return DuplicateSourceDocument.valid.filter(pk__in=queryset)

    def get_duplicates_of(self, document, permission=None, user=None):
        DuplicateTargetDocument = apps.get_model(
            app_label='duplicates', model_name='DuplicateTargetDocument'
        )

        queryset = DuplicateTargetDocument.valid.none()

        when_list = []

        for entry in self.filter(document=document).all():
            queryset = queryset | DuplicateTargetDocument.valid.filter(
                pk__in=entry.documents.only('pk').values('pk')
            )

            when_list.append(
                models.When(
                    Q(pk__in=entry.documents.only('pk').values('pk')),
                    then=Value(value=str(entry.stored_backend))
                )
            )

        queryset = queryset.annotate(
            backend=models.Case(
                *when_list, output_field=models.CharField()
            )
        )

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset, user=user
            )

        return queryset
