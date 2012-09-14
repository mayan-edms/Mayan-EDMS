from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_app
from .permissions import PERMISSION_BACKUP_JOB_VIEW, PERMISSION_BACKUP_JOB_CREATE, PERMISSION_BACKUP_JOB_EDIT, PERMISSION_BACKUP_JOB_DELETE

backup_tool_link = Link(text=_(u'backups'), view='backup_job_list', icon='cd_burn.png', permissions=[PERMISSION_BACKUP_JOB_VIEW])
backup_job_list = Link(text=_(u'backup job list'), view='backup_job_list', sprite='cd_burn', permissions=[PERMISSION_BACKUP_JOB_VIEW])
backup_job_create = Link(text=_(u'create'), view='backup_job_create', sprite='cd_add', permissions=[PERMISSION_BACKUP_JOB_CREATE])
backup_job_edit = Link(text=_(u'edit'), view='backup_job_edit', args='object.pk', sprite='cd_edit', permissions=[PERMISSION_BACKUP_JOB_EDIT])
backup_job_test = Link(text=_(u'test'), view='backup_job_test', args='object.pk', sprite='cd_go')#, permissions=[PERMISSION_BACKUP_JOB_TEST])
backup_job_delete = Link(text=_(u'delete'), view='backup_job_delete', args='object.pk', sprite='cd_delete', permissions=[PERMISSION_BACKUP_JOB_DELETE])

restore_tool_link = Link(text=_(u'restore'), view='restore_view', icon='cd_eject.png')#, permissions=[])
