from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class OrganizationDocumentTypeSettingsManager(models.Manager):
    def get_queryset(self):
        DocumentType = apps.get_model('documents', 'DocumentType')

        return super(
            OrganizationDocumentTypeSettingsManager, self
        ).get_queryset().filter(
            document_type__in=DocumentType.on_organization.all(),
        )


class OrganizationDocumentVersionOCRErrorManager(models.Manager):
    def get_queryset(self):
        DocumentVersion = apps.get_model('documents', 'DocumentVersion')

        return super(
            OrganizationDocumentVersionOCRErrorManager, self
        ).get_queryset().filter(
            document_version__in=DocumentVersion.on_organization.all(),
        )


class OrganizationDocumentPageContentManager(models.Manager):
    def get_queryset(self):
        DocumentPage = apps.get_model('documents', 'DocumentPage')

        return super(
            OrganizationDocumentPageContentManager, self
        ).get_queryset().filter(
            document_page__in=DocumentPage.on_organization.all(),
        )
