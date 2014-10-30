from django.utils.translation import ugettext_lazy as _

from acls.classes import EncapsulatedObject

from .models import DocumentTypeMetadataType, MetadataType


class MetadataClass(object):
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def __getattr__(self, name):
        if name in self.dictionary:
            return self.dictionary.get(name)
        else:
            raise AttributeError(_(u'\'metadata\' object has no attribute \'%s\'') % name)


class MetadataObjectWrapper(EncapsulatedObject):
    source_object_name = u'metadata_object'


class DocumentTypeMetadataTypeManager(object):
    @staticmethod
    @property
    def factory(document_type):
        instance = DocumentTypeMetadataTypeManager(document_type)
        return instance

    def __init__(self, document_type):
        self.document_type = document_type

    def filter(self, **kwargs):
        return self.get_query_set(**kwargs)

    def all(self):
        return self.get_query_set()

    def get_query_set(self, **kwargs):
        try:
            return MetadataType.objects.filter(pk__in=self.document_type.documenttypemetadatatype_set.filter(**kwargs).values_list('metadata_type', flat=True))
        except self.document_type.documenttypemetadatatype_set.model.DoesNotExist:
            return MetadataType.objects.none()

    def add(self, metadata_type, required=False):
        DocumentTypeMetadataType.objects.create(document_type=self.document_type, metadata_type= metadata_type, required=required)

    def remove(self, metadata_type):
        DocumentTypeMetadataType.objects.get(document_type=self.document_type, metadata_type= metadata_type).delete()
