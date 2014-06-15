from __future__ import absolute_import


def cleanup():
    from .models import MetadataType, MetadataSet

    MetadataType.objects.all().delete()
    MetadataSet.objects.all().delete()
