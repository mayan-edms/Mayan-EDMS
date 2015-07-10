from __future__ import unicode_literals, absolute_import

import logging

from permissions.models import StoredPermission

logger = logging.getLogger(__name__)


class ModelPermission(object):
    _registry = {}
    _proxies = {}
    _inheritances = {}

    @classmethod
    def register(cls, model, permissions):
        cls._registry.setdefault(model, [])
        for permission in permissions:
            cls._registry[model].append(permission)

    @classmethod
    def get_for_instance(cls, instance):
        try:
            permissions = cls._registry[type(instance)]
        except KeyError:
            try:
                permissions = cls._registry[cls._proxies[type(instance)]]
            except KeyError:
                permissions = ()

        pks = [permission.stored_permission.pk for permission in permissions]
        return StoredPermission.objects.filter(pk__in=pks)

    @classmethod
    def register_proxy(cls, source, model):
        cls._proxies[model] = source

    @classmethod
    def register_inheritance(cls, model, related):
        cls._inheritances[model] = related

    @classmethod
    def get_inheritance(cls, model):
        return cls._inheritances[model]
