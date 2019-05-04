from __future__ import absolute_import

from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from mayan.apps.acls.models import AccessControlList
from mayan.apps.permissions import Permission


class MayanPermission(BasePermission):
    def has_permission(self, request, view):
        required_permissions = getattr(
            view, 'mayan_view_permissions', {}
        ).get(request.method, None)

        if required_permissions:
            try:
                Permission.check_user_permissions(
                    permissions=required_permissions, user=request.user
                )
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        required_permissions = getattr(
            view, 'mayan_object_permissions', {}
        ).get(request.method, None)

        if required_permissions:
            try:
                AccessControlList.objects.check_access(
                    obj=obj, permissions=required_permissions,
                    user=request.user
                )
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True
