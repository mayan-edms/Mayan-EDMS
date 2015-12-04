from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext

from permissions.models import StoredPermission

from .classes import ModelPermission

logger = logging.getLogger(__name__)


class AccessControlListManager(models.Manager):
    """
    Implement a 3 tier permission system, involving a permissions, an actor
    and an object
    """

    def get_inherited_permissions(self, role, obj):
        try:
            instance = obj.first()
        except AttributeError:
            instance = obj
        else:
            if not instance:
                return StoredPermission.objects.none()

        try:
            parent_accessor = ModelPermission.get_inheritance(type(instance))
        except KeyError:
            return StoredPermission.objects.none()
        else:
            parent_object = getattr(instance, parent_accessor)
            content_type = ContentType.objects.get_for_model(parent_object)
            try:
                return self.get(
                    role=role, content_type=content_type,
                    object_id=parent_object.pk
                ).permissions.all()
            except self.model.DoesNotExist:
                return StoredPermission.objects.none()

    def check_access(self, permissions, user, obj, related=None):
        if user.is_superuser or user.is_staff:
            return True

        try:
            stored_permissions = [
                permission.stored_permission for permission in permissions
            ]
        except TypeError:
            stored_permissions = [permissions.stored_permission]

        if related:
            obj = getattr(obj, related)

        try:
            parent_accessor = ModelPermission.get_inheritance(obj._meta.model)
        except KeyError:
            pass
        else:
            try:
                return self.check_access(
                    permissions, user, getattr(obj, parent_accessor)
                )
            except PermissionDenied:
                pass

        user_roles = []
        for group in user.groups.all():
            for role in group.roles.all():
                if set(stored_permissions).intersection(set(self.get_inherited_permissions(role=role, obj=obj))):
                    return True

                user_roles.append(role)

        # TODO: possible .exists() optimization
        if not self.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, permissions__in=stored_permissions, role__in=user_roles):
            raise PermissionDenied(ugettext('Insufficient access.'))

    def filter_by_access(self, permission, user, queryset):
        if user.is_superuser or user.is_staff:
            return queryset

        user_roles = []
        for group in user.groups.all():
            for role in group.roles.all():
                user_roles.append(role)

        try:
            parent_accessor = ModelPermission.get_inheritance(queryset.model)
        except KeyError:
            parent_acl_query = Q()
        else:
            instance = queryset.first()
            if instance:
                parent_object = getattr(instance, parent_accessor)
                parent_content_type = ContentType.objects.get_for_model(
                    parent_object
                )
                parent_queryset = self.filter(
                    content_type=parent_content_type, role__in=user_roles,
                    permissions=permission.stored_permission
                )
                parent_acl_query = Q(
                    **{
                        '{}__pk__in'.format(
                            parent_accessor
                        ): parent_queryset.values_list('object_id', flat=True)
                    }
                )
            else:
                parent_acl_query = Q()

        # Directly granted access
        content_type = ContentType.objects.get_for_model(queryset.model)
        acl_query = Q(pk__in=self.filter(
            content_type=content_type, role__in=user_roles,
            permissions=permission.stored_permission
        ).values_list('object_id', flat=True))

        return queryset.filter(parent_acl_query | acl_query)
