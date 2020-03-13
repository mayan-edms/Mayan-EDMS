from __future__ import unicode_literals, absolute_import

import itertools
import logging

from django.apps import apps
from django.utils.encoding import force_text

from mayan.apps.common.utils import get_related_field

logger = logging.getLogger(name=__name__)


class ModelPermission(object):
    _functions = {}
    _inheritances = {}
    _inheritances_reverse = {}
    _manager_names = {}
    _registry = {}

    @classmethod
    def deregister(cls, model):
        cls._registry.pop(model, None)

    @classmethod
    def get_classes(cls, as_content_type=False):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        if as_content_type:
            content_type_dictionary = ContentType.objects.get_for_models(
                *cls._registry.keys()
            )
            content_type_ids = [
                content_type.pk for content_type in content_type_dictionary.values()
            ]

            return ContentType.objects.filter(pk__in=content_type_ids)
        else:
            return cls._registry.keys()

    @classmethod
    def get_for_class(cls, klass, as_choices=False):
        if as_choices:
            results = []

            for namespace, permissions in itertools.groupby(cls.get_for_class(klass=klass, as_choices=False), lambda entry: entry.namespace):
                permission_options = [
                    (force_text(permission.pk), permission) for permission in permissions
                ]
                results.append(
                    (namespace, permission_options)
                )

            return results
        else:
            # Return the permissions for the klass and the models that
            # inherit from it.
            result = []
            result.extend(cls._registry.get(klass, ()))
            for model in cls._inheritances_reverse.get(klass, ()):
                result.extend(cls._registry.get(model, ()))

            return result

    @classmethod
    def get_for_instance(cls, instance):
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        permissions = []

        class_permissions = cls.get_for_class(klass=type(instance))

        if class_permissions:
            permissions.extend(class_permissions)

        pks = [
            permission.stored_permission.pk for permission in set(permissions)
        ]
        return StoredPermission.objects.filter(pk__in=pks)

    @classmethod
    def get_function(cls, model):
        return cls._functions[model]

    @classmethod
    def get_inheritance(cls, model):
        # Proxy models get the inheritance from their base model
        if model._meta.proxy:
            model = model._meta.proxy_for_model

        return cls._inheritances[model]

    @classmethod
    def get_manager(cls, model):
        try:
            manager_name = cls.get_manager_name(model=model)
        except KeyError:
            manager_name = None

        if manager_name:
            manager = getattr(model, manager_name)
        else:
            manager = model._meta.default_manager

        return manager

    @classmethod
    def get_manager_name(cls, model):
        return cls._manager_names[model]

    @classmethod
    def register(cls, model, permissions):
        from django.contrib.contenttypes.fields import GenericRelation

        cls._registry.setdefault(model, [])
        for permission in permissions:
            cls._registry[model].append(permission)

        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        model.add_to_class(
            name='acls', value=GenericRelation(AccessControlList)
        )

    @classmethod
    def register_function(cls, model, function):
        cls._functions[model] = function

    @classmethod
    def register_inheritance(cls, model, related):
        model_reverse = get_related_field(
            model=model, related_field_name=related
        ).related_model
        cls._inheritances_reverse.setdefault(model_reverse, [])
        cls._inheritances_reverse[model_reverse].append(model)

        cls._inheritances[model] = related

    @classmethod
    def register_manager(cls, model, manager_name):
        cls._manager_names[model] = manager_name
