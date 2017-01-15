from __future__ import unicode_literals

import logging

from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from .exceptions import InvalidNamespace

logger = logging.getLogger(__name__)


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

    def __unicode__(self):
        return unicode(self.label)

    def add_permission(self, name, label):
        permission = Permission(namespace=self, name=name, label=label)
        self.permissions.append(permission)
        return permission


class Permission(object):
    _stored_permissions_cache = {}
    _permissions = {}

    @classmethod
    def invalidate_cache(cls):
        cls._stored_permissions_cache = {}

    @classmethod
    def check_permissions(cls, requester, permissions):
        try:
            for permission in permissions:
                if permission.stored_permission.requester_has_this(requester):
                    return True
        except TypeError:
            # Not a list of permissions, just one
            if permissions.stored_permission.requester_has_this(requester):
                return True

        logger.debug('no permission')

        raise PermissionDenied(_('Insufficient permissions.'))

    @classmethod
    def get_for_holder(cls, holder):
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        return StoredPermission.get_for_holder(holder)

    @classmethod
    def all(cls):
        # Return sorted permisions by namespace.name
        return sorted(
            cls._permissions.values(), key=lambda x: x.namespace.name
        )

    @classmethod
    def get(cls, get_dict, proxy_only=False):
        if 'pk' in get_dict:
            if proxy_only:
                return cls._permissions[get_dict['pk']]
            else:
                return cls._permissions[get_dict['pk']].stored_permission

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.pk = self.uuid
        self.__class__._permissions[self.uuid] = self

    def __unicode__(self):
        return unicode(self.label)

    def __str__(self):
        return str(self.__unicode__())

    @property
    def uuid(self):
        return '%s.%s' % (self.namespace.name, self.name)

    @property
    def stored_permission(self):
        StoredPermission = apps.get_model(
            app_label='permissions', model_name='StoredPermission'
        )

        try:
            return self.__class__._stored_permissions_cache[self.uuid]
        except KeyError:
            stored_permission, created = StoredPermission.objects.get_or_create(
                namespace=self.namespace.name,
                name=self.name,
            )
            stored_permission.volatile_permission = self
            self.__class__._stored_permissions_cache[
                self.uuid
            ] = stored_permission
            return stored_permission
