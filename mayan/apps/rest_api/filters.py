from __future__ import absolute_import, unicode_literals

from rest_framework.filters import BaseFilterBackend

from mayan.apps.acls.models import AccessControlList


class MayanObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # TODO: fix variable name to make it clear it should be a single
        # permission

        required_permissions = getattr(
            view, 'mayan_object_permissions', {}
        ).get(request.method, None)

        if required_permissions:
            return AccessControlList.objects.restrict_queryset(
                queryset=queryset, permission=required_permissions[0],
                user=request.user
            )
        else:
            return queryset


class MayanViewSetObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Filter the API view queryset by access using a permission.
        Requires the object_permission_map class attribute which is a dictionary
        that matches a view action ('update', 'list', etc) to a single
        permission instance.
        Example: object_permission_map = {
            'update': permission_..._edit
            'list': permission_..._view
        }
        """
        if not request.user or not request.user.is_authenticated:
            return queryset.none()

        object_permission_dictionary = getattr(view, 'object_permission_map', {})
        object_permission = object_permission_dictionary.get(
            view.action, None
        )

        if object_permission:
            return AccessControlList.objects.restrict_queryset(
                permission=object_permission, queryset=queryset,
                user=request.user
            )
        else:
            return queryset
