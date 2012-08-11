from __future__ import absolute_import

from django.db import transaction, DatabaseError
from django.utils.translation import ugettext_lazy as _

from job_processor.models import JobQueue, JobType
from job_processor.exceptions import JobQueuePushError
from navigation.api import bind_links
from project_tools.api import register_tool

from .links import backup_tool_link, restore_tool_link

# TODO: move to literals
BACKUP_JOB_QUEUE_NAME = 'backups_queue'


@transaction.commit_on_success
def create_backups_job_queue():
    global backups_job_queue
    try:
        backups_job_queue, created = JobQueue.objects.get_or_create(name=BACKUP_JOB_QUEUE_NAME, defaults={'label': _('Backups'), 'unique_jobs': True})
    except DatabaseError:
        transaction.rollback()


create_backups_job_queue()
#backup_job_type = JobType('remote_backup', _(u'Remove backup'), do_backup)

register_tool(backup_tool_link)
register_tool(restore_tool_link)
