from __future__ import unicode_literals

import itertools
import logging

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .exceptions import InvalidNamespace

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class PermissionNamespace(object):
    _registry = {}

    @classmethod
    def all(cls):
        return cls._registry.values()

    @classmethod
    def get(cls, name):
        try:
            return cls._registry[name]
        except KeyError:
            raise InvalidNamespace(
                'Invalid namespace name. This is probably an obsolete '
                'permission namespace, execute the management command '
                '"purgepermissions" and try again.'
            )

    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.permissions = []
        self.__class__._registry[name] = self

    def __str__(self):
        return force_text(self.label)

    def add_permission(self, name, label):
        permission = Permission(namespace=self, name=name, label=label)
        self.permissions.append(permission)
        return permission


@python_2_unicode_compatible
class Permission(object):
    _permissions = {}
    _stored_permissions_cache = {}

    @classmethod
    def all(cls, as_choices=False):
        if as_choices:
            results = []

            for namespace, permissions in itertools.groupby(cls.all(), lambda entry: entry.namespace):
                permission_options = [
                    (force_text(permission.pk), permission) for permission in permissions
                ]
                results.append(
                    (namespace, permission_options)
                )

            return results
        else:
            # Return sorted permisions by namespace.name
            return sorted(
                cls._permissions.values(), key=lambda x: x.namespace.name
            )

    @classmethod
    def check_user_permissions(cls, permissions, user):
        for permission in permissions:
            if permission.stored_permission.user_has_this(user=user):
                return True

        logger.debug(
            'User "%s" does not have permissions "%s"', user, permissions
        )
        raise PermissionDenied(_('Insufficient permissions.'))

    @classmethod
    def get(cls, pk, proxy_only=False):
        if proxy_only:
            return cls._permissions[pk]
        else:
            return cls._permissions[pk].stored_permission

    @classmethod
    def invalidate_cache(cls):
        cls._stored_permissions_cache = {}

    @classmethod
    def refresh(cls):
        for permission in cls.all():
            permission.stored_permission

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.pk = self.get_pk()
        self.__class__._permissions[self.pk] = self

    def __repr__(self):
        return self.pk

    def __str__(self):
        return force_text(self.label)

    def get_pk(self):
        return '%s.%s' % (self.namespace.name, self.name)

    @property
    def stored_permission(self):
        try:
            return self.__class__._stored_permissions_cache[self.pk]
        except KeyError:
            StoredPermission = apps.get_model(
                app_label='permissions', model_name='StoredPermission'
            )

            stored_permission, created = StoredPermission.objects.get_or_create(
                namespace=self.namespace.name,
                name=self.name,
            )

            self.__class__._stored_permissions_cache[self.pk] = stored_permission
            return stored_permission
