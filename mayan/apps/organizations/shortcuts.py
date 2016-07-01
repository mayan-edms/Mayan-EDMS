from __future__ import unicode_literals

from django.apps import apps


def get_current_organization():
    Organization = apps.get_model('organizations', 'Organization')
    return Organization.objects.get_current().pk
