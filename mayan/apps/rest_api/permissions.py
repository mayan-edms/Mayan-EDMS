from __future__ import absolute_import

from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from acls.models import AccessEntry
from permissions.models import Permission


class MayanPermission(BasePermission):
    def has_permission(self, request, view):
        if hasattr(view, 'mayan_view_permissions'):
            try:
                Permission.objects.check_permissions(request.user, view.mayan_view_permissions)
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if hasattr(view, 'mayan_object_permissions'):
            try:
                Permission.objects.check_permissions(request.user, view.mayan_object_permissions)
            except PermissionDenied:
                try:
                    if hasattr(view, 'mayan_permission_attribute_check'):
                        AccessEntry.objects.check_accesses(view.mayan_object_permissions, request.user, getattr(obj, view.mayan_permission_attribute_check))
                    else:
                        AccessEntry.objects.check_accesses(view.mayan_object_permissions, request.user, obj)
                except PermissionDenied:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True
