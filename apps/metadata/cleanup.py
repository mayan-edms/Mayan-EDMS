from __future__ import absolute_import

from .models import MetadataType, MetadataSet


def cleanup():
    MetadataType.objects.all().delete()
    MetadataSet.objects.all().delete()
