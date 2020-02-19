from __future__ import absolute_import, unicode_literals

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


class MayanViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Block the API view by access using a permission.
        Requires the view_permission_map class attribute which is a dictionary
        that matches a view actions ('create', 'destroy', etc) to a single
        permission instance.
        Example: view_permission_map = {
            'update': permission_..._edit
            'list': permission_..._view
        }
        """
        if not request.user or not request.user.is_authenticated:
            return False

        view_permission_dictionary = getattr(view, 'view_permission_map', {})
        view_permission = view_permission_dictionary.get(view.action, None)

        if view_permission:
            try:
                Permission.check_user_permissions(
                    permissions=(view_permission,), user=request.user
                )
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True
