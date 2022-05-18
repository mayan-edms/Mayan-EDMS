from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_signature_capture_create, icon_signature_capture_single_delete,
    icon_signature_capture_edit, icon_signature_capture_list
)
from .permissions import (
    permission_signature_capture_create, permission_signature_capture_delete,
    permission_signature_capture_edit, permission_signature_capture_view
)

link_signature_capture_create = Link(
    args='object.pk', icon=icon_signature_capture_create, permissions=(
        permission_signature_capture_create,
    ), text=_('Create new signature capture'),
    view='signature_captures:signature_capture_create'
)
link_signature_capture_delete = Link(
    args='object.pk', icon=icon_signature_capture_single_delete,
    permissions=(permission_signature_capture_delete,), tags='dangerous',
    text=_('Delete'),
    view='signature_captures:signature_capture_delete'
)
link_signature_capture_edit = Link(
    args='object.id', icon=icon_signature_capture_edit,
    permissions=(permission_signature_capture_edit,), text=_('Edit'),
    view='signature_captures:signature_capture_edit'
)
link_signature_capture_list = Link(
    args='resolved_object.pk', icon=icon_signature_capture_list,
    permissions=(permission_signature_capture_view,), text=_(
        'Signature captures'
    ), view='signature_captures:signature_capture_list'
)
