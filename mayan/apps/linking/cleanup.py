from __future__ import absolute_import


def cleanup():
    from .models import SmartLink

    SmartLink.objects.all().delete()
