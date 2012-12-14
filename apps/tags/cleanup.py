from __future__ import absolute_import

from taggit.models import Tag


def delete_all_tags():
    Tag.objects.all().delete()
