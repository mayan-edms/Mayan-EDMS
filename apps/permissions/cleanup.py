from __future__ import absolute_import

from .models import Role, PermissionHolder


def cleanup():
    Role.objects.all().delete()
