from django.utils.translation import ugettext_lazy as _

from .models import MetadataType


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
