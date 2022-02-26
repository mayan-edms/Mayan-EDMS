from rest_framework.filters import BaseFilterBackend, OrderingFilter

from mayan.apps.acls.models import AccessControlList


class MayanObjectPermissionsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        permission = self.get_mayan_object_permissions(request=request, view=view)

        if permission:
            return AccessControlList.objects.restrict_queryset(
                queryset=queryset, permission=permission,
                user=request.user
            )
        else:
            return queryset

    def get_mayan_object_permissions(self, request, view):
        try:
            return getattr(view, 'get_mayan_object_permissions')()
        except AttributeError:
            return getattr(
                view, 'mayan_object_permissions', {}
            ).get(request.method, (None,))[0]


class MayanSortingFilter(OrderingFilter):
    ordering_param = '_ordering'

    def get_default_valid_fields(self, queryset, view, context={}):
        return ()
