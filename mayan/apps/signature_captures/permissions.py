from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Signature captures'), name='signature_captures'
)

permission_signature_capture_create = namespace.add_permission(
    label=_('Create signature captures'),
    name='signature_capture_create'
)
permission_signature_capture_delete = namespace.add_permission(
    label=_('Delete signature captures'),
    name='signature_capture_delete'
)
permission_signature_capture_edit = namespace.add_permission(
    label=_('Edit signature captures'),
    name='signature_capture_edit'
)
permission_signature_capture_view = namespace.add_permission(
    label=_('View signature captures'),
    name='signature_capture_view'
)
