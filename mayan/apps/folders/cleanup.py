from __future__ import absolute_import


def cleanup():
    from .models import Folder
    Folder.objects.all().delete()
