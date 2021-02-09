from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions.classes import PermissionNamespace

namespace = PermissionNamespace(label=_('Quotas'), name='quotas')

permission_quota_create = namespace.add_permission(
    label=_('Create a quota'), name='quota_create'
)
permission_quota_delete = namespace.add_permission(
    label=_('Delete a quota'), name='quota_delete'
)
permission_quota_edit = namespace.add_permission(
    label=_('Edit a quota'), name='quota_edit'
)
permission_quota_view = namespace.add_permission(
    label=_('View a quota'), name='quota_view'
)
