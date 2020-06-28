from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Common'), name='common')

permission_object_copy = namespace.add_permission(
    label=_('Copy object'), name='object_copy'
)
