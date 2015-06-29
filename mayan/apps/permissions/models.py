from __future__ import unicode_literals

import logging

from django.contrib.auth.models import Group, User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from .managers import RoleMemberManager, StoredPermissionManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class StoredPermission(models.Model):
    namespace = models.CharField(max_length=64, verbose_name=_('Namespace'))
    name = models.CharField(max_length=64, verbose_name=_('Name'))

    objects = StoredPermissionManager()

    class Meta:
        ordering = ('namespace',)
        unique_together = ('namespace', 'name')
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')

    def __init__(self, *args, **kwargs):
        from .classes import Permission

        super(StoredPermission, self).__init__(*args, **kwargs)
        try:
            self.volatile_permission = Permission.get({'pk': '%s.%s' % (self.namespace, self.name)}, proxy_only=True)
        except KeyError:
            # Must be a deprecated permission in the database that is no
            # longer used in the current code
            pass

    def __str__(self):
        return unicode(getattr(self, 'volatile_permission', self.name))

    def get_holders(self):
        return self.roles.all()
        #return (holder.holder_object for holder in self.permissionholder_set.all())

    def requester_has_this(self, actor):
        #actor = AnonymousUserSingleton.objects.passthru_check(actor)

        logger.debug('actor: %s', actor)
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


@python_2_unicode_compatible
class Role(models.Model):
    name = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=64, unique=True, verbose_name=_('Label'))
    permissions = models.ManyToManyField(StoredPermission, related_name='roles', verbose_name=_('Permissions'))
    groups = models.ManyToManyField(Group, related_name='roles', verbose_name=_('Groups'))

    class Meta:
        ordering = ('label',)
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('permissions:role_list')
