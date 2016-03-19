from __future__ import unicode_literals, absolute_import

import logging

from django.apps import apps

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
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        permissions = []

        class_permissions = cls._registry.get(type(instance))

        if class_permissions:
            permissions.extend(class_permissions)

        proxy = cls._proxies.get(type(instance))

        if proxy:
            permissions.extend(cls._registry.get(proxy))

        pks = [permission.stored_permission.pk for permission in set(permissions)]
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
