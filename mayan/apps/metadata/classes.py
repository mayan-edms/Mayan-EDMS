from django.utils.translation import ugettext_lazy as _

from acls.classes import EncapsulatedObject

from .models import DocumentMetadata, DocumentTypeMetadataType, MetadataType


class DocumentTypeMetadataTypeHelper(object):
    @staticmethod
    @property
    def constructor(source_object):
        return DocumentTypeMetadataTypeHelper(source_object)

    def __init__(self, instance):
        self.instance = instance

    def filter(self, **kwargs):
        return self.get_query_set(**kwargs)

    def all(self):
        return self.get_query_set()

    def get_query_set(self, **kwargs):
        try:
            return MetadataType.objects.filter(pk__in=self.instance.documenttypemetadatatype_set.filter(**kwargs).values_list('metadata_type', flat=True))
        except MetadataType.DoesNotExist:
            return MetadataType.objects.none()

    def add(self, metadata_type, required=False):
        DocumentTypeMetadataType.objects.create(document_type=self.instance, metadata_type=metadata_type, required=required)

    def remove(self, metadata_type):
        DocumentTypeMetadataType.objects.get(document_type=self.instance, metadata_type=metadata_type).delete()


class DocumentMetadataHelper(object):
    @staticmethod
    @property
    def constructor(source_object):
        return DocumentMetadataHelper(source_object)

    def __init__(self, instance):
        self.instance = instance

    def __getattr__(self, name):
        try:
            return self.instance.metadata.get(metadata_type__name=name).value
        except MetadataType.DoesNotExist:
            raise AttributeError(_(u'\'metadata\' object has no attribute \'%s\'') % name)

