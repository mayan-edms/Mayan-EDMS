from __future__ import absolute_import

from .models import History


def cleanup():
    History.objects.all().delete()
