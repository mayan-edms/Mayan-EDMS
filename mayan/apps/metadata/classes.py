from django.utils.translation import ugettext_lazy as _

from .models import DocumentTypeMetadataType, MetadataType
from .tasks import task_add_required_metadata_type, task_remove_metadata_type


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
            return MetadataType.objects.filter(pk__in=self.instance.metadata.filter(**kwargs).values_list('metadata_type', flat=True))
        except MetadataType.DoesNotExist:
            return MetadataType.objects.none()

    def add(self, metadata_type, required=False):
        if metadata_type not in self.instance.metadata_type.all():
            DocumentTypeMetadataType.objects.create(document_type=self.instance, metadata_type=metadata_type, required=required)
            if required:
                task_add_required_metadata_type.apply_async(kwargs={'metadata_type_id': metadata_type.pk, 'document_type_id': self.instance.pk}, queue='metadata')

    def remove(self, metadata_type):
        DocumentTypeMetadataType.objects.get(document_type=self.instance, metadata_type=metadata_type).delete()
        task_remove_metadata_type.apply_async(kwargs={'metadata_type_id': metadata_type.pk, 'document_type_id': self.instance.pk}, queue='metadata')


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
