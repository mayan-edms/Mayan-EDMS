from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('document_states', _('States'))
PERMISSION_WORKFLOW_CREATE = Permission.objects.register(namespace, 'workflow_create', _('Create workflows'))
PERMISSION_WORKFLOW_DELETE = Permission.objects.register(namespace, 'workflow_delte', _('Delete workflows'))
PERMISSION_WORKFLOW_EDIT = Permission.objects.register(namespace, 'workflow_edit', _('Edit workflows'))
PERMISSION_WORKFLOW_VIEW = Permission.objects.register(namespace, 'workflow_view', _('View workflows'))

PERMISSION_DOCUMENT_WORKFLOW_VIEW = Permission.objects.register(namespace, 'document_workflow_view', _('View document workflows'))
PERMISSION_DOCUMENT_WORKFLOW_TRANSITION = Permission.objects.register(namespace, 'document_workflow_transition', _('Transition document workflows'))
