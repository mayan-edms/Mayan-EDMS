from __future__ import unicode_literals, absolute_import

import logging

logger = logging.getLogger(__name__)


class ModelPermission(object):
    _registry = {}

    @classmethod
    def register(cls, model, permissions):
        cls._registry.setdefault(model, [])
        for permission in permissions:
            cls._registry[model].append(permission.stored_permission.pk)

    @classmethod
    def get_for_instance(cls, instance):
        from permissions.models import StoredPermission

        pks = cls._registry.get(type(instance), ())
        return StoredPermission.objects.filter(pk__in=pks)
