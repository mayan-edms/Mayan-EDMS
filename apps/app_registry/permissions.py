from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from permissions.models import PermissionNamespace, Permission

namespace = PermissionNamespace('backups', _(u'Backups'))

PERMISSION_BACKUP_JOB_VIEW = Permission.objects.register(namespace, 'backup_job_view', _(u'View a backup job'))
PERMISSION_BACKUP_JOB_CREATE = Permission.objects.register(namespace, 'backup_job_view', _(u'Create backup jobs'))
PERMISSION_BACKUP_JOB_EDIT = Permission.objects.register(namespace, 'backup_job_edit', _(u'Edit an existing backup jobs'))
PERMISSION_BACKUP_JOB_DELETE = Permission.objects.register(namespace, 'backup_job_delete', _(u'Delete an existing backup jobs'))
