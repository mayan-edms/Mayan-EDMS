from __future__ import absolute_import


def cleanup():
    from .models import Index
    Index.objects.all().delete()
