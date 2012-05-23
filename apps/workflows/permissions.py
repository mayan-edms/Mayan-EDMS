from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('workflows', _(u'Workflows'))

PERMISSION_WORKFLOW_SETUP_VIEW = Permission.objects.register(namespace, 'workflow_setup_view', _(u'View existing workflow templates'))
PERMISSION_WORKFLOW_SETUP_CREATE = Permission.objects.register(namespace, 'workflow_setup_create', _(u'Create new workflow templates'))
PERMISSION_WORKFLOW_SETUP_EDIT = Permission.objects.register(namespace, 'workflow_setup_edit', _(u'Edit existing workflow templates'))
PERMISSION_WORKFLOW_SETUP_DELETE = Permission.objects.register(namespace, 'workflow_setup_delete', _(u'Delete existing workflow templates'))

PERMISSION_WORKFLOW_RUN = Permission.objects.register(namespace, 'workflow_setup_run', _(u'Execute a workflow'))

#PERMISSION_STATE_SETUP_VIEW = Permission.objects.register(namespace, 'state_setup_view', _(u'View existing states'))
#PERMISSION_STATE_SETUP_CREATE = Permission.objects.register(namespace, 'state_setup_create', _(u'Create new state templates'))
#PERMISSION_STATE_SETUP_EDIT = Permission.objects.register(namespace, 'state_setup_edit', _(u'Edit existing state templates'))
#PERMISSION_STATE_SETUP_DELETE = Permission.objects.register(namespace, 'state_setup_delete', _(u'Delete existing state templates'))

#PERMISSION_TRANSITION_SETUP_VIEW = Permission.objects.register(namespace, 'transition_setup_view', _(u'View existing transition templates'))
#PERMISSION_TRANSITION_SETUP_CREATE = Permission.objects.register(namespace, 'transition_setup_create', _(u'Create new transition templates'))
#PERMISSION_TRANSITION_SETUP_EDIT = Permission.objects.register(namespace, 'transition_setup_edit', _(u'Edit existing transition templates'))
#PERMISSION_TRANSITION_SETUP_DELETE = Permission.objects.register(namespace, 'transition_setup_delete', _(u'Delete existing transition templates'))

