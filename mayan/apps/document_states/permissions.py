from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions import PermissionNamespace

namespace = PermissionNamespace('document_states', _('Document workflows'))

permission_workflow_create = namespace.add_permission(
    name='workflow_create', label=_('Create workflows')
)
permission_workflow_delete = namespace.add_permission(
    name='workflow_delte', label=_('Delete workflows')
)
permission_workflow_edit = namespace.add_permission(
    name='workflow_edit', label=_('Edit workflows')
)
permission_workflow_view = namespace.add_permission(
    name='workflow_view', label=_('View workflows')
)
permission_document_workflow_view = namespace.add_permission(
    name='document_workflow_view', label=_('View document workflows')
)
permission_document_workflow_transition = namespace.add_permission(
    name='document_workflow_transition',
    label=_('Transition document workflows')
)
