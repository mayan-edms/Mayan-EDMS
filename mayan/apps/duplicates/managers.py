import logging

from django.apps import apps
from django.db import models
from django.db.models import Q, Value

from mayan.apps.acls.models import AccessControlList
from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError

from .classes import DuplicateBackend

logger = logging.getLogger(name=__name__)


class StoredDuplicateBackendManager(models.Manager):
    def scan_document(self, document):
        """
        Find duplicates of document based on each registered backend's logic.
        """
        lock_name = 'duplicates__scan_document-{}'.format(document.pk)
        try:
            logger.debug('trying to acquire lock: %s', lock_name)
            lock = LockingBackend.get_backend().acquire_lock(name=lock_name)
            logger.debug('acquired lock: %s', lock_name)
            try:
                DuplicateBackendEntry = apps.get_model(
                    app_label='duplicates', model_name='DuplicateBackendEntry'
                )

                for backend_path, backend_class in DuplicateBackend.get_all():
                    if backend_class.verify(document=document):

                        stored_backend, created = self.get_or_create(
                            backend_path=backend_path
                        )
                        duplicates = stored_backend.get_backend_instance().process(
                            document=document
                        )

                        if duplicates.exists():
                            duplicates_entry, created = stored_backend.duplicate_entries.get_or_create(
                                document=document
                            )

                            bulk_create_list = [
                                duplicates_entry.documents.through(
                                    duplicatebackendentry_id=duplicates_entry.pk,
                                    document=duplicate
                                ) for duplicate in duplicates
                            ]

                            duplicates_entry.documents.through.objects.bulk_create(
                                bulk_create_list, ignore_conflicts=True
                            )

                            # Create empty duplicate entries for the
                            # duplicates as source that do not have one.
                            bulk_create_list = [
                                DuplicateBackendEntry(
                                    stored_backend=stored_backend,
                                    document=duplicate,
                                ) for duplicate in duplicates.filter(
                                    duplicates__stored_backend=None
                                )
                            ]

                            DuplicateBackendEntry.objects.bulk_create(
                                bulk_create_list, ignore_conflicts=True
                            )

                            # Get all duplicate entries for the duplicates as
                            # source.
                            duplicate_entries = stored_backend.duplicate_entries.filter(
                                document__in=duplicates
                            )

                            # Create the many to many entries for this
                            # document as a target.
                            bulk_create_list = [
                                document.as_duplicate.through(
                                    duplicatebackendentry_id=duplicate_entry.pk,
                                    document_id=document.pk
                                ) for duplicate_entry in duplicate_entries
                            ]

                            document.as_duplicate.through.objects.bulk_create(
                                bulk_create_list, ignore_conflicts=True
                            )
                        else:
                            # Document has no duplicates for this backend.
                            # Delete any existing entry for where this
                            # document is the source for the backend.
                            stored_backend.duplicate_entries.filter(
                                document=document
                            ).delete()

                            # Delete any existing entry for where this
                            # document is a duplicate for the backend.
                            document.as_duplicate.filter(
                                stored_backend=stored_backend
                            ).delete()
                    else:
                        # Document cannot be scanned for duplicates for this
                        # backend. Delete any existing entries for the
                        # backend where the document is a source or target.
                        stored_backend.duplicate_entries.filter(
                            documents=document
                        ).delete()

                        document.as_duplicate.filter(
                            stored_backend=stored_backend
                        ).delete()
            finally:
                lock.release()
        except LockError:
            logger.debug('unable to obtain lock: %s' % lock_name)
            raise


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
