from __future__ import unicode_literals, absolute_import

import logging

from permissions.models import StoredPermission

logger = logging.getLogger(__name__)


class ModelPermission(object):
    _registry = {}

    @classmethod
    def register(cls, model, permissions):
        cls._registry.setdefault(model, [])
        for permission in permissions:
            cls._registry[model].append(permission)

    @classmethod
    def get_for_instance(cls, instance):
        permissions = cls._registry.get(type(instance), ())
        pks = [permission.stored_permission.pk for permission in permissions]
        return StoredPermission.objects.filter(pk__in=pks)
