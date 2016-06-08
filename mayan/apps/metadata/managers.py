from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class MetadataTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class OrganizationDocumentMetadataManager(models.Manager):
    def get_queryset(self):
        Document = apps.get_model('documents', 'Document')
        MetadataType = apps.get_model('metadata', 'MetadataType')

        return super(
            OrganizationDocumentMetadataManager, self
        ).get_queryset().filter(
            document__in=Document.on_organization.all(),
            metadata_type__in=MetadataType.on_organization.all()
        )


class OrganizationDocumentTypeMetadataTypeManager(models.Manager):
    def get_queryset(self):
        DocumentType = apps.get_model('documents', 'DocumentType')
        MetadataType = apps.get_model('metadata', 'MetadataType')

        return super(
            OrganizationDocumentTypeMetadataTypeManager, self
        ).get_queryset().filter(
            document_type__in=DocumentType.on_organization.all(),
            metadata_type__in=MetadataType.on_organization.all()
        )
