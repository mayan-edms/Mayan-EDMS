from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Announcements'), name='announcements'
)

permission_announcement_create = namespace.add_permission(
    label=_('Create announcements'), name='announcement_create'
)
permission_announcement_delete = namespace.add_permission(
    label=_('Delete announcements'), name='announcement_delete'
)
permission_announcement_edit = namespace.add_permission(
    label=_('Edit announcements'), name='announcement_edit'
)
permission_announcement_view = namespace.add_permission(
    label=_('View announcements'), name='announcement_view'
)
