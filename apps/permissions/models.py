from __future__ import absolute_import

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from common.models import AnonymousUserSingleton

from .managers import (RoleMemberManager, StoredPermissionManager)

logger = logging.getLogger(__name__)


class PermissionNamespace(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label

    def __unicode__(self):
        return unicode(self.label)


class PermissionDoesNotExists(Exception):
    pass


class PermissionManager(object):
    _permissions = {}
    DoesNotExist = PermissionDoesNotExists()

    @classmethod
    def register(cls, namespace, name, label):
        permission = Permission(namespace, name, label)
        cls._permissions[permission.uuid] = permission
        return permission

    @classmethod
    def check_permissions(cls, requester, permission_list):
        for permission in permission_list:
            if permission.requester_has_this(requester):
                return True

        logger.debug('no permission')

        raise PermissionDenied(ugettext(u'Insufficient permissions.'))

    @classmethod
    def get_for_holder(cls, holder):
        return StoredPermission.objects.get_for_holder(holder)

    @classmethod
    def all(cls):
        # Return sorted permisions by namespace.name
        return sorted(cls._permissions.values(), key=lambda x: x.namespace.name)

    @classmethod
    def get(cls, get_dict, proxy_only=False):
        if 'pk' in get_dict:
            try:
                if proxy_only:
                    return cls._permissions[get_dict['pk']]
                else:
                    return cls._permissions[get_dict['pk']].get_stored_permission()
            except KeyError:
                raise Permission.DoesNotExist

    def __init__(self, model):
        self.model = model


class Permission(object):
    _stored_permissions_cache = {}
    
    DoesNotExist = PermissionDoesNotExists

    def __init__(self, namespace, name, label):
        self.namespace = namespace
        self.name = name
        self.label = label
        self.pk = self.uuid

    def __unicode__(self):
        return unicode(self.label)

    def __str__(self):
        return str(self.__unicode__())

    @property
    def uuid(self):
        return u'%s.%s' % (self.namespace.name, self.name)

    @property
    def stored_permission(self):
        return self.get_stored_permission()

    def get_stored_permission(self):
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
        stored_permission = self.get_stored_permission()
        return stored_permission.requester_has_this(requester)

    def save(self, *args, **kwargs):
        return self.get_stored_permission()

Permission.objects = PermissionManager(Permission)
Permission._default_manager = Permission.objects


class StoredPermission(models.Model):
    namespace = models.CharField(max_length=64, verbose_name=_(u'namespace'))
    name = models.CharField(max_length=64, verbose_name=_(u'name'))

    objects = StoredPermissionManager()

    class Meta:
        ordering = ('namespace', )
        unique_together = ('namespace', 'name')
        verbose_name = _(u'permission')
        verbose_name_plural = _(u'permissions')

    def __init__(self, *args, **kwargs):
        super(StoredPermission, self).__init__(*args, **kwargs)
        self.volatile_permission = Permission.objects.get({'pk': '%s.%s' % (self.namespace, self.name)}, proxy_only=True)

    def __unicode__(self):
        return unicode(getattr(self, 'volatile_permission', self.name))

    def get_holders(self):
        return (holder.holder_object for holder in self.permissionholder_set.all())

    def requester_has_this(self, actor):
        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        logger.debug('actor: %s' % actor)
        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return True

        # Request is one of the permission's holders?
        if actor in self.get_holders():
            return True

        # If not check if the requesters memberships objects is one of
        # the permission's holder?
        roles = RoleMember.objects.get_roles_for_member(actor)

        if isinstance(actor, User):
            groups = actor.groups.all()
        else:
            groups = []

        for membership in list(set(roles) | set(groups)):
            if self.requester_has_this(membership):
                return True

        logger.debug('Fallthru')
        return False

    def grant_to(self, actor):
        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        permission_holder, created = PermissionHolder.objects.get_or_create(permission=self, holder_type=ContentType.objects.get_for_model(actor), holder_id=actor.pk)
        return created

    def revoke_from(self, actor):
        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        try:
            permission_holder = PermissionHolder.objects.get(permission=self, holder_type=ContentType.objects.get_for_model(actor), holder_id=actor.pk)
            permission_holder.delete()
        except PermissionHolder.DoesNotExist:
            return False
        else:
            return True


class PermissionHolder(models.Model):
    permission = models.ForeignKey(StoredPermission, verbose_name=_(u'permission'))
    holder_type = models.ForeignKey(ContentType,
        related_name='permission_holder',
        limit_choices_to={'model__in': ('user', 'group', 'role')})
    holder_id = models.PositiveIntegerField()
    holder_object = generic.GenericForeignKey(ct_field='holder_type', fk_field='holder_id')

    class Meta:
        verbose_name = _(u'permission holder')
        verbose_name_plural = _(u'permission holders')

    def __unicode__(self):
        return u'%s: %s' % (self.holder_type, self.holder_object)


class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64, unique=True, verbose_name=_(u'label'))

    class Meta:
        ordering = ('label',)
        verbose_name = _(u'role')
        verbose_name_plural = _(u'roles')

    def __unicode__(self):
        return self.label

    @models.permalink
    def get_absolute_url(self):
        return ('role_list',)

    def add_member(self, member):
        member = AnonymousUserSingleton.objects.passthru_check(member)
        role_member, created = RoleMember.objects.get_or_create(
            role=self,
            member_type=ContentType.objects.get_for_model(member),
            member_id=member.pk)
        if not created:
            raise Exception('Unable to add member to role')

    def remove_member(self, member):
        member = AnonymousUserSingleton.objects.passthru_check(member)
        member_type = ContentType.objects.get_for_model(member)
        role_member = RoleMember.objects.get(role=self, member_type=member_type, member_id=member.pk)
        role_member.delete()

    def members(self, filter_dict=None):
        filter_dict = filter_dict or {}
        return (member.member_object for member in self.rolemember_set.filter(**filter_dict) if member is None)
        # return (member.member_object for member in self.rolemember_set.filter(**filter_dict))  >>>>>> hotfix/v0.12.3


class RoleMember(models.Model):
    role = models.ForeignKey(Role, verbose_name=_(u'role'))
    member_type = models.ForeignKey(ContentType,
        related_name='role_member',
        limit_choices_to={
            'model__in': (
                'user', 'group', 'anonymoususersingleton'
            )
        }
    )
    member_id = models.PositiveIntegerField()
    member_object = generic.GenericForeignKey(ct_field='member_type', fk_field='member_id')

    objects = RoleMemberManager()

    class Meta:
        #ordering = ('label',)
        verbose_name = _(u'role member')
        verbose_name_plural = _(u'role members')

    def __unicode__(self):
        return unicode(self.member_object)
