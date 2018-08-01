from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class MetadataTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def get_for_document(self, document):
        return self.filter(
            pk__in=document.metadata.values_list(
                'metadata_type', flat=True
            )
        )

    def get_for_document_type(self, document_type):
        return self.filter(
            pk__in=document_type.metadata.values_list(
                'metadata_type', flat=True
            )
        )


class DocumentTypeMetadataTypeManager(models.Manager):
    def get_by_natural_key(self, metadata_type_name, document_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        try:
            document = Document.objects.get_by_natural_key(document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist

        return document.metadata.get(metadata_type_name=metadata_type_name)

    def get_metadata_types_for(self, document_type):
        DocumentType = apps.get_model(
            app_label='metadata', model_name='MetadataType'
        )

        return DocumentType.objects.filter(
            pk__in=self.filter(
                document_type=document_type
            ).values_list('metadata_type__pk', flat=True)
        )
