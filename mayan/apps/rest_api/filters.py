from rest_framework.filters import BaseFilterBackend, OrderingFilter

from mayan.apps.acls.models import AccessControlList


class MayanObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
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


class MayanSortingFilter(OrderingFilter):
    ordering_param = '_ordering'

    def get_default_valid_fields(self, queryset, view, context={}):
        return ()
