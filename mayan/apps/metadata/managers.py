from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class MetadataTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def get_for_document(self, document):
        return self.filter(document_metadata__document=document)

    def get_for_document_type(self, document_type):
        return self.filter(document_type_relations__document_type=document_type)


class DocumentTypeMetadataTypeManager(models.Manager):
    def get_by_natural_key(self, document_natural_key, metadata_type_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        MetadataType = apps.get_model(
            app_label='metadata', model_name='MetadataType'
        )
        try:
            document = Document.objects.get_by_natural_key(document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist
        else:
            try:
                metadata_type = MetadataType.objects.get_by_natural_key(metadata_type_natural_key)
            except MetadataType.DoesNotExist:
                raise self.model.DoesNotExist

        return self.get(document__pk=document.pk, metadata_type__pk=metadata_type.pk)

    def get_metadata_types_for(self, document_type):
        DocumentType = apps.get_model(
            app_label='metadata', model_name='MetadataType'
        )

        return DocumentType.objects.filter(
            pk__in=self.filter(
                document_type=document_type
            ).values_list('metadata_type__pk', flat=True)
        )
