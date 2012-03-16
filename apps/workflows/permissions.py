from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

user_management_namespace = PermissionNamespace('workflows', _(u'Workflows'))

PERMISSION_WORKFLOW_SETUP_VIEW = Permission.objects.register(user_management_namespace, 'workflow_setup_view', _(u'View existing workflows templates'))
