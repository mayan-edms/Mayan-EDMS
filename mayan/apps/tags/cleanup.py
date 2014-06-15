from __future__ import absolute_import

from taggit.models import Tag


def cleanup():
    Tag.objects.all().delete()
