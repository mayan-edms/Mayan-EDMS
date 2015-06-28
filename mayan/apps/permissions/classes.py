from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied

from acls.classes import EncapsulatedObject

from .models import StoredPermission


class Member(EncapsulatedObject):
    source_object_name = 'member_object'


class PermissionNamespace(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label

    def __unicode__(self):
        return unicode(self.label)

    def add_permission(self, name, label):
        return Permission(namespace=self, name=name, label=label)


class Permission(object):
    _stored_permissions_cache = {}
    _permissions = {}

    @classmethod
    def check_permissions(cls, requester, permission_list):
        for permission in permission_list:
            if permission.requester_has_this(requester):
                return True

        logger.debug('no permission')

        raise PermissionDenied(ugettext('Insufficient permissions.'))

    @classmethod
    def get_for_holder(cls, holder):
        return StoredPermission.get_for_holder(holder)

    @classmethod
    def all(cls):
        # Return sorted permisions by namespace.name
        return sorted(cls._permissions.values(), key=lambda x: x.namespace.name)

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
        try:
            return self.__class__._stored_permissions_cache[self]
        except KeyError:
            stored_permission, created = StoredPermission.objects.get_or_create(
                namespace=self.namespace.name,
                name=self.name,
            )
            stored_permission.volatile_permission = self
            self.__class__._stored_permissions_cache[self] = stored_permission
            return stored_permission

    def requester_has_this(self, requester):
        stored_permission = self.stored_permission
        return stored_permission.requester_has_this(requester)
