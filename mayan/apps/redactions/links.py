from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .permissions import (
    permission_redaction_create, permission_redaction_delete,
    permission_redaction_edit, permission_redaction_view
)

link_redaction_create = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redaction_create',
    permissions=(permission_redaction_create,), text=_('Create redaction'),
    view='redactions:redaction_create', args='resolved_object.id'
)
link_redaction_delete = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redaction_delete',
    permissions=(permission_redaction_delete,), tags='dangerous',
    text=_('Delete'), view='redactions:redaction_delete',
    args='resolved_object.id'
)
link_redaction_edit = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redaction_edit',
    permissions=(permission_redaction_edit,), text=_('Edit'),
    view='redactions:redaction_edit', args='resolved_object.id'
)
link_redaction_list = Link(
    icon_class_path='mayan.apps.redactions.icons.icon_redactions',
    permissions=(permission_redaction_view,), text=_('Redactions'),
    view='redactions:redaction_list', args='resolved_object.id'
)
