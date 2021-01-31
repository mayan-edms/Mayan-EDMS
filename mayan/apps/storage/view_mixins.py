from mayan.apps.acls.models import AccessControlList
from mayan.apps.permissions.models import StoredPermission


class RelatedObjectPermissionViewMixin:
    def get_source_queryset(self):
        queryset = super().get_source_queryset()
        permission_values = queryset.values('permission')
        stored_permission_queryset = StoredPermission.objects.filter(
            pk__in=permission_values
        )

        result = queryset.none()
        for stored_permission in stored_permission_queryset:
            result = result | AccessControlList.objects.restrict_queryset(
                permission=stored_permission.volatile_permission,
                queryset=queryset, user=self.request.user
            )

        result = result | queryset.filter(permission__isnull=True)
        return result.distinct()
