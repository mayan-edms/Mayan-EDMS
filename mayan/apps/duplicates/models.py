import logging

from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import BackendModelMixin
from mayan.apps.documents.models.document_models import Document

from .classes import NullBackend
from .managers import (
    DuplicateBackendEntryManager, StoredDuplicateBackendManager
)

logger = logging.getLogger(name=__name__)


class StoredDuplicateBackend(BackendModelMixin, models.Model):
    _backend_model_null_backend = NullBackend

    objects = StoredDuplicateBackendManager()

    class Meta:
        verbose_name = _('Stored duplicate backend')
        verbose_name_plural = _('Stored duplicate backends')

    def __str__(self):
        return str(self.get_backend_label())

    def get_absolute_url(self):
        return reverse(
            viewname='duplicates:backend_detail', kwargs={
                'backend_id': self.pk
            }
        )

    def get_duplicated_documents(
        self, permission=None, source_document=None, user=None
    ):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DuplicateSourceDocument = apps.get_model(
            app_label='duplicates', model_name='DuplicateSourceDocument'
        )

        if source_document:
            try:
                document_stored_backend = source_document.duplicates.get(
                    stored_backend=self
                )
            except DuplicateBackendEntry.DoesNotExist:
                queryset = DuplicateTargetDocument.objects.none()
            else:
                queryset = Document.valid.filter(
                    id__in=document_stored_backend.documents.all()
                )
        else:
            queryset = DuplicateTargetDocument.valid.filter(
                as_duplicate__stored_backend=self
            ).distinct()

        if permission:
            queryset = AccessControlList.objects.restrict_queryset(
                permission=permission, queryset=queryset, user=user
            )

        return DuplicateSourceDocument.valid.filter(id__in=queryset)


class DocumentStoredDuplicateBackend(StoredDuplicateBackend):
    class Meta:
        proxy = True


class DuplicateBackendEntry(models.Model):
    stored_backend = models.ForeignKey(
        on_delete=models.CASCADE, related_name='duplicate_entries',
        to=StoredDuplicateBackend, verbose_name=_('Stored duplicate backend')
    )
    document = models.ForeignKey(
        on_delete=models.CASCADE, related_name='duplicates', to=Document,
        verbose_name=_('Document')
    )
    documents = models.ManyToManyField(
        related_name='as_duplicate', to=Document, verbose_name=_(
            'Duplicated documents'
        )
    )

    objects = DuplicateBackendEntryManager()

    class Meta:
        unique_together = ('stored_backend', 'document')
        verbose_name = _('Duplicated backend entry')
        verbose_name_plural = _('Duplicated backend entries')


class DuplicateSourceDocument(Document):
    class Meta:
        proxy = True


class DuplicateTargetDocument(Document):
    class Meta:
        proxy = True
