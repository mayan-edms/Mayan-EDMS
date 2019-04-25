from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model


def get_user_queryset():
    return get_user_model().objects.filter(is_superuser=False, is_staff=False)
