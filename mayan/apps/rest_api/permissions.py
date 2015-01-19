from __future__ import absolute_import

from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied

from rest_framework.permissions import BasePermission

from acls.models import AccessEntry
from permissions.models import Permission


class MayanPermission(BasePermission):
    def has_permission(self, request, view):
        required_permission = getattr(view, 'mayan_view_permissions', {}).get(request.method, None)

        if required_permission:
            try:
                Permission.objects.check_permissions(request.user, required_permission)
            except PermissionDenied:
                return False
            else:
                return True
        else:
            return True

    def has_object_permission(self, request, view, obj):
        required_permission = getattr(view, 'mayan_object_permissions', {}).get(request.method, None)

        if required_permission:
            try:
                Permission.objects.check_permissions(request.user, required_permission)
            except PermissionDenied:
                try:
                    if hasattr(view, 'mayan_permission_attribute_check'):
                        AccessEntry.objects.check_accesses(required_permission, request.user, getattr(obj, view.mayan_permission_attribute_check))
                    else:
                        AccessEntry.objects.check_accesses(required_permission, request.user, obj)
                except PermissionDenied:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True
