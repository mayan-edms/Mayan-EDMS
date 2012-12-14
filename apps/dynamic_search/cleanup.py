from __future__ import absolute_import

from .models import RecentSearch


def cleanup():
    RecentSearch.objects.all().delete()
