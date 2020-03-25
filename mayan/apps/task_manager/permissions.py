from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Task manager'), name='task_manager')

permission_task_view = namespace.add_permission(
    label=_('View tasks'), name='task_view'
)
