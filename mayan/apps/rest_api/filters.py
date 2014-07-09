from __future__ import absolute_import

from rest_framework.filters import BaseFilterBackend

from acls.models import AccessEntry
from permissions.models import Permission


class MayanObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if hasattr(view, 'mayan_object_permissions'):
            try:
                Permission.objects.check_permissions(request.user, view.mayan_object_permissions)
            except PermissionDenied:
                return AccessEntry.objects.filter_objects_by_access(view.mayan_object_permissions[0], request.user, queryset)
            else:
                return queryset
        else:
            return queryset

