from __future__ import absolute_import

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from common.models import AnonymousUserSingleton
from permissions.models import Permission

from .classes import EncapsulatedObject, AccessHolder, ClassAccessHolder

logger = logging.getLogger(__name__)


class AccessEntryManager(models.Manager):
    """
    Implement a 3 tier permission system, involving a permissions, an actor
    and an object
    """
    def source_object(self, obj):
        if isinstance(obj, EncapsulatedObject):
            return obj.source_object
        else:
            return obj

    def grant(self, permission, actor, obj):
        """
        Grant a permission (what), (to) an actor, (on) a specific object
        """
        obj = self.source_object(obj)
        actor = self.source_object(actor)

        access_entry, created = self.model.objects.get_or_create(
            permission=permission,
            holder_type=ContentType.objects.get_for_model(actor),
            holder_id=actor.pk,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk
        )
        return created

    def revoke(self, permission, actor, obj):
        """
        Revoke a permission (what), (from) an actor, (on) a specific object
        """
        obj = self.source_object(obj)
        actor = self.source_object(actor)

        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
            access_entry.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def has_access(self, permission, actor, obj):
        """
        Returns whether an actor has a specific permission for an object
        """
        obj = self.source_object(obj)
        actor = self.source_object(actor)

        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return True

        actor = AnonymousUserSingleton.objects.passthru_check(actor)

        try:
            self.model.objects.get(
                permission=permission.get_stored_permission(),
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
        except self.model.DoesNotExist:
            return False
        else:
            return True

    def check_access(self, permission, actor, obj):
        # TODO: Merge with has_access
        obj = self.source_object(obj)
        actor = self.source_object(actor)

        if self.has_access(permission, actor, obj):
            return True
        else:
            raise PermissionDenied(ugettext(u'Insufficient access.'))

    def check_accesses(self, permission_list, actor, obj):
        """
        Returns whether an actor has at least one of a list of permissions for an object
        """
        obj = self.source_object(obj)
        actor = self.source_object(actor)
        for permission in permission_list:
            if self.has_access(permission, actor, obj):
                return True

        raise PermissionDenied(ugettext(u'Insufficient access.'))

    def get_allowed_class_objects(self, permission, actor, cls, related=None):
        logger.debug('related: %s' % related)

        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        actor_type = ContentType.objects.get_for_model(actor)
        content_type = ContentType.objects.get_for_model(cls)
        if related:
            master_list = [obj.content_object for obj in self.model.objects.select_related().filter(holder_type=actor_type, holder_id=actor.pk, permission=permission.get_stored_permission)]
            logger.debug('master_list: %s' % master_list)
            # TODO: update to use Q objects and check performance diff
            # kwargs = {'%s__in' % related: master_list}
            # Q(**kwargs)
            return (obj for obj in cls.objects.all() if getattr(obj, related) in master_list)
        else:
            return (obj.content_object for obj in self.model.objects.filter(holder_type=actor_type, holder_id=actor.pk, content_type=content_type, permission=permission.get_stored_permission))

    def get_acl_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_list', args=[content_type.app_label, content_type.model, obj.pk])

    def get_new_holder_url(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return reverse('acl_new_holder_for', args=[content_type.app_label, content_type.model, obj.pk])

    def get_holders_for(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type, object_id=obj.pk):
            entry = AccessHolder.encapsulate(access_entry.holder_object)

            if entry not in holder_list:
                holder_list.append(entry)

        return holder_list

    def get_holder_permissions_for(self, obj, actor):
        """
        Returns a list of actors that hold at least one permission for
        a specific object
        """
        logger.debug('obj: %s' % obj)
        logger.debug('actor: %s' % actor)

        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return Permission.objects.all()

        actor_type = ContentType.objects.get_for_model(actor)
        content_type = ContentType.objects.get_for_model(obj)
        return (access.permission for access in self.model.objects.filter(content_type=content_type, object_id=obj.pk, holder_type=actor_type, holder_id=actor.pk))

    def filter_objects_by_access(self, permission, actor, object_list, exception_on_empty=False, related=None):
        """
        Filter a list of objects or a QuerySet elements depending on
        whether the actor holds the specified permission
        """
        logger.debug('exception_on_empty: %s' % exception_on_empty)
        logger.debug('object_list: %s' % object_list)

        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return object_list

        try:
            if object_list.count() == 0:
                return object_list
        except TypeError:
            # object_list is not a queryset
            if len(object_list) == 0:
                return object_list

        try:
            # Try to process as a QuerySet
            qs = object_list.filter(pk__in=[obj.pk for obj in self.get_allowed_class_objects(permission, actor, object_list[0].__class__, related)])
            logger.debug('qs: %s' % qs)

            if qs.count() == 0 and exception_on_empty == True:
                raise PermissionDenied

            return qs
        except AttributeError:
            # Fallback to a filtered list
            object_list = list(set(object_list) & set(self.get_allowed_class_objects(permission, actor, object_list[0].__class__, related)))
            logger.debug('object_list: %s' % object_list)
            if len(object_list) == 0 and exception_on_empty == True:
                raise PermissionDenied

            return object_list


class DefaultAccessEntryManager(models.Manager):
    """
    Implement a 3 tier permission system, involving a permission, an actor
    and a class or content type.  This model keeps track of the access
    control lists that will be added when an instance of the recorded
    content type is created.
    """
    def get_holders_for(self, cls):
        if isinstance(cls, EncapsulatedObject):
            cls = cls.source_object

        content_type = ContentType.objects.get_for_model(cls)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type):
            entry = ClassAccessHolder.encapsulate(access_entry.holder_object)

            if entry not in holder_list:
                holder_list.append(entry)

        return holder_list

    def has_access(self, permission, actor, cls):
        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return True

        try:
            self.model.objects.get(
                permission=permission.get_stored_permission(),
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=ContentType.objects.get_for_model(cls),
            )
        except self.model.DoesNotExist:
            return False
        else:
            return True

    def grant(self, permission, actor, cls):
        """
        Grant a permission (what), (to) an actor, (on) a specific class
        """
        access_entry, created = self.model.objects.get_or_create(
            permission=permission,
            holder_type=ContentType.objects.get_for_model(actor),
            holder_id=actor.pk,
            content_type=ContentType.objects.get_for_model(cls),
        )
        return created

    def revoke(self, permission, actor, cls):
        """
        Revoke a permission (what), (from) an actor, (on) a specific class
        """
        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=ContentType.objects.get_for_model(cls),
            )
            access_entry.delete()
            return True
        except self.model.DoesNotExist:
            return False

    def get_holder_permissions_for(self, cls, actor):
        if isinstance(actor, User):
            if actor.is_superuser or actor.is_staff:
                return Permission.objects.all()

        actor_type = ContentType.objects.get_for_model(actor)
        content_type = ContentType.objects.get_for_model(cls)
        return [access.permission for access in self.model.objects.filter(content_type=content_type, holder_type=actor_type, holder_id=actor.pk)]
