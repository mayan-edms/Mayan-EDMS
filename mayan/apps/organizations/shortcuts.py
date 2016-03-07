from __future__ import unicode_literals

from django.apps import apps


def get_current_organization():
    from .models import Organization
    return Organization.objects.get_current().pk
