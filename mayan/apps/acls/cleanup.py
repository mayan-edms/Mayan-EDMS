from __future__ import absolute_import

from .models import AccessEntry, DefaultAccessEntry


def cleanup():
    AccessEntry.objects.all().delete()
    DefaultAccessEntry.objects.all().delete()
