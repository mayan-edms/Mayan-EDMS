from __future__ import absolute_import

from django.contrib.auth.models import User, Group


def cleanup():
    User.objects.exclude(is_staff=True).exclude(is_superuser=True).delete()
    Group.objects.all().delete()
