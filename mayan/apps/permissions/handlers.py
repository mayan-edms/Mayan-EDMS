from __future__ import unicode_literals

from django.apps import apps

from .classes import Permission


def handler_permission_initialize(**kwargs):
    Permission.initialize()


def handler_purge_permissions(**kwargs):
    StoredPermission = apps.get_model(
        app_label='permissions', model_name='StoredPermission'
    )

    StoredPermission.objects.purge_obsolete()
