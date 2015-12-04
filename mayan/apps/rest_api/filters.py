from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied

from rest_framework.filters import BaseFilterBackend

from acls.models import AccessControlList
from permissions import Permission


class MayanObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        required_permission = getattr(
            view, 'mayan_object_permissions', {}
        ).get(request.method, None)

        if required_permission:
            try:
                Permission.check_permissions(request.user, required_permission)
            except PermissionDenied:
                return AccessControlList.objects.filter_by_access(
                    required_permission[0], request.user, queryset
                )
            else:
                return queryset
        else:
            return queryset
