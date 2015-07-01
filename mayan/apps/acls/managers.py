from __future__ import absolute_import, unicode_literals

import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext

from permissions import Permission

logger = logging.getLogger(__name__)


class AccessControlListManager(models.Manager):
    """
    Implement a 3 tier permission system, involving a permissions, an actor
    and an object
    """

    def check_access(self, permissions, user, obj):
        if user.is_superuser or user.is_staff:
            return True

        user_roles = []
        for group in user.groups.all():
            for role in group.roles.all():
                user_roles.append(role)

        try:
            stored_permissions = [permission.stored_permission for permission in permissions]
        except TypeError:
            stored_permissions = [permissions.stored_permission]

        if not self.filter(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk, permissions__in=stored_permissions, role__in=user_roles):
            raise PermissionDenied(ugettext('Insufficient access.'))

    def filter_by_access(self, permission, user, queryset,  exception_on_empty=False, related=None):
        if user.is_superuser or user.is_staff:
            return queryset

        user_roles = []
        for group in user.groups.all():
            for role in group.roles.all():
                user_roles.append(role)

        content_type = ContentType.objects.get_for_model(queryset.model)

        acls = self.filter(content_type=content_type, role__in=user_roles, permissions=permission.stored_permission).values_list('object_id', flat=True)

        new_queryset = queryset.filter(pk__in=acls)

        if new_queryset.count() == 0 and exception_on_empty:
            raise PermissionDenied

        return new_queryset
