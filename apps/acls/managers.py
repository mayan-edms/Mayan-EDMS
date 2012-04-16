from __future__ import absolute_import

import logging

from django.db import models
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q

from common.models import AnonymousUserSingleton
from permissions.models import Permission, RoleMember

from .classes import AccessHolder, ClassAccessHolder, get_source_object

logger = logging.getLogger(__name__)


class AccessEntryManager(models.Manager):
    """
    Implement a 3 tier permission system, involving a permissions, an actor
    and an object
    """
    def grant(self, permission, actor, obj):
        """
        Grant a permission (what), (to) an actor, (on) a specific object
        """
        obj = get_source_object(obj)
        actor = get_source_object(actor)

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
        obj = get_source_object(obj)
        actor = get_source_object(actor)

        try:
            access_entry = self.model.objects.get(
                permission=permission,
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.pk
            )
        except self.model.DoesNotExist:
            return False
        else:
            access_entry.delete()
            return True

    def has_access(self, permission, actor, obj, db_only=False):
        """
        Returns whether an actor has a specific permission for an object
        """
        obj = get_source_object(obj)
        actor = get_source_object(actor)

        if isinstance(actor, User) and db_only == False:
            # db_only causes the return of only the stored permissions
            # and not the perceived permissions for an actor
            if actor.is_superuser or actor.is_staff:
                return True

        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        try:
            content_type=ContentType.objects.get_for_model(obj)
        except AttributeError:
            # Object doesn't have a content type, therefore allow access
            return True

        try:
            self.model.objects.get(
                permission=permission.get_stored_permission(),
                holder_type=ContentType.objects.get_for_model(actor),
                holder_id=actor.pk,
                content_type=content_type,
                object_id=obj.pk
            )
        except self.model.DoesNotExist:
            # If not check if the actor's memberships is one of
            # the access's holder?
            roles = RoleMember.objects.get_roles_for_member(actor)

            if isinstance(actor, User):
                groups = actor.groups.all()
            else:
                groups = []

            for membership in list(set(roles) | set(groups)):
                if self.has_access(permission, membership, obj, db_only):
                    return True

            logger.debug('Fallthru')
            return False
        else:
            return True

    def check_access(self, permission, actor, obj):
        # TODO: Merge with has_access
        obj = get_source_object(obj)
        actor = get_source_object(actor)

        if self.has_access(permission, actor, obj):
            return True
        else:
            raise PermissionDenied(ugettext(u'Insufficient access.'))

    def check_accesses(self, permission_list, actor, obj):
        """
        Returns whether an actor has at least one of a list of permissions for an object
        """
        obj = get_source_object(obj)
        actor = get_source_object(actor)
        for permission in permission_list:
            if self.has_access(permission, actor, obj):
                return True

        raise PermissionDenied(ugettext(u'Insufficient access.'))

    def get_allowed_class_objects(self, permission, actor, cls, related=None):
        logger.debug('related: %s' % related)

        actor = AnonymousUserSingleton.objects.passthru_check(actor)
        actor_type = ContentType.objects.get_for_model(actor)
        content_type = ContentType.objects.get_for_model(cls)

        # Calculate actor role membership ACL query
        total_queries = Q()
        for role in RoleMember.objects.get_roles_for_member(actor):
            role_type = ContentType.objects.get_for_model(role)
            if related:
                query = Q(holder_type=role_type, holder_id=role.pk, permission=permission.get_stored_permission)
            else:
                query = Q(holder_type=role_type, holder_id=role.pk, content_type=content_type, permission=permission.get_stored_permission)
            if not total_queries:
                total_queries = query
            else:
                total_queries = total_queries | query

        # Calculate actor group membership ACL query
        if isinstance(actor, User):
            groups = actor.groups.all()
        else:
            groups = []

        for group in groups:
            group_type = ContentType.objects.get_for_model(group)
            if related:
                query = Q(holder_type=group_type, holder_id=group.pk, permission=permission.get_stored_permission)
            else:
                query = Q(holder_type=group_type, holder_id=group.pk, content_type=content_type, permission=permission.get_stored_permission)
            if not total_queries:
                total_queries = query
            else:
                total_queries = total_queries | query

        if related:
            actor_query = Q(holder_type=actor_type, holder_id=actor.pk, permission=permission.get_stored_permission)
            master_list = [obj.content_object for obj in self.model.objects.select_related().filter(actor_query | total_queries)]
            logger.debug('master_list: %s' % master_list)
            # TODO: update to use Q objects and check performance diff
            # kwargs = {'%s__in' % related: master_list}
            # Q(**kwargs)
            return (obj for obj in cls.objects.all() if getattr(obj, related) in master_list)
        else:
            actor_query = Q(holder_type=actor_type, holder_id=actor.pk, content_type=content_type, permission=permission.get_stored_permission)
            return (obj.content_object for obj in self.model.objects.filter(actor_query | total_queries))

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
            if access_entry.holder_object:
                # Don't add references to non existant content type objects
                entry = AccessHolder.encapsulate(access_entry.holder_object)

                if entry not in holder_list:
                    holder_list.append(entry)

        return holder_list

    def get_holder_permissions_for(self, obj, actor, db_only=False):
        """
        Returns a list of actors that hold at least one permission for
        a specific object
        """
        logger.debug('obj: %s' % obj)
        logger.debug('actor: %s' % actor)

        if isinstance(actor, User) and db_only == False:
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
        cls = get_source_object(cls)
        content_type = ContentType.objects.get_for_model(cls)
        holder_list = []
        for access_entry in self.model.objects.filter(content_type=content_type):
            if access_entry.holder_object:
                # Don't add references to non existant content type objects
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
