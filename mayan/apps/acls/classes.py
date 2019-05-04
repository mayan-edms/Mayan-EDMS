from __future__ import unicode_literals, absolute_import

import logging

from django.apps import apps

logger = logging.getLogger(__name__)


class ModelPermission(object):
    _functions = {}
    _inheritances = {}
    _registry = {}

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
    def get_classes(cls, as_content_type=False):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        if as_content_type:
            content_type_dictionary = ContentType.objects.get_for_models(
                models=cls._registry.keys()
            )
            content_type_ids = [
                content_type.pk for content_type in content_type_dictionary.values()
            ]

            return ContentType.objects.filter(pk__in=content_type_ids)
        else:
            return cls._registry.keys()

    @classmethod
    def get_for_class(cls, klass):
        return cls._registry.get(klass, ())

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
        return cls._inheritances[model]

    @classmethod
    def register_function(cls, model, function):
        cls._functions[model] = function

    @classmethod
    def register_inheritance(cls, model, related):
        cls._inheritances[model] = related
