from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Logging'), name='logging')

permission_error_log_entry_delete = namespace.add_permission(
    label=_('Delete error log'), name='error_log_delete'
)
permission_error_log_entry_view = namespace.add_permission(
    label=_('View error log'), name='error_log_view'
)
