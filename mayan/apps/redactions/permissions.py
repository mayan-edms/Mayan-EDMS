from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Redactions'), name='redactions')

permission_redaction_create = namespace.add_permission(
    label=_('Create new redactions'), name='redaction_create'
)
permission_redaction_delete = namespace.add_permission(
    label=_('Delete redactions'), name='redaction_delete'
)
permission_redaction_edit = namespace.add_permission(
    label=_('Edit redactions'), name='redaction_edit'
)
permission_redaction_exclude = namespace.add_permission(
    label=_('Exclude redactions'), name='redaction_exclude'
)
permission_redaction_view = namespace.add_permission(
    label=_('View existing redactions'), name='redaction_view'
)
