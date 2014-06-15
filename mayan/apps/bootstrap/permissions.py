from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('bootstrap', _(u'Database bootstrap'))

PERMISSION_BOOTSTRAP_VIEW = Permission.objects.register(namespace, 'bootstrap_view', _(u'View bootstrap setups'))
PERMISSION_BOOTSTRAP_CREATE = Permission.objects.register(namespace, 'bootstrap_create', _(u'Create bootstrap setups'))
PERMISSION_BOOTSTRAP_EDIT = Permission.objects.register(namespace, 'bootstrap_edit', _(u'Edit bootstrap setups'))
PERMISSION_BOOTSTRAP_DELETE = Permission.objects.register(namespace, 'bootstrap_delete', _(u'Delete bootstrap setups'))
PERMISSION_BOOTSTRAP_EXECUTE = Permission.objects.register(namespace, 'bootstrap_execute', _(u'Execute bootstrap setups'))
PERMISSION_BOOTSTRAP_DUMP = Permission.objects.register(namespace, 'bootstrap_dump', _(u'Dump the current project\s setup into a bootstrap setup'))
PERMISSION_BOOTSTRAP_EXPORT = Permission.objects.register(namespace, 'bootstrap_export', _(u'Export bootstrap setups as files'))
PERMISSION_BOOTSTRAP_IMPORT = Permission.objects.register(namespace, 'bootstrap_import', _(u'Import new bootstrap setups'))
PERMISSION_BOOTSTRAP_REPOSITORY_SYNC = Permission.objects.register(namespace, 'bootstrap_repo_sync', _(u'Sync the local bootstrap setups with a published repository'))
PERMISSION_NUKE_DATABASE = Permission.objects.register(namespace, 'nuke_database', _(u'Erase the entire database and document storage'))
