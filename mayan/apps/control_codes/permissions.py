from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Control codes'), name='control_codes'
)
permission_control_sheet_create = namespace.add_permission(
    label=_('Create new control sheets'), name='control_sheet_create'
)
permission_control_sheet_delete = namespace.add_permission(
    label=_('Delete control sheets'), name='control_sheet_delete'
)
permission_control_sheet_edit = namespace.add_permission(
    label=_('Edit control sheets'), name='control_sheet_edit'
)
permission_control_sheet_view = namespace.add_permission(
    label=_('View existing control sheets'), name='control_sheet_view'
)
