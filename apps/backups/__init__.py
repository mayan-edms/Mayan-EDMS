from __future__ import absolute_import

import inspect

from django.conf import settings
from django.db import transaction, DatabaseError
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

#from common.utils import encapsulate
#from job_processor.exceptions import JobQueuePushError
#from job_processor.models import JobQueue, JobType
#from project_tools.api import register_tool
#from project_setup.api import register_setup
#from navigation.api import bind_links, register_model_list_columns

#from .classes import AppBackup, ModelBackup

#from .links import (app_registry_tool_link, app_list, backup_tool_link, 
#    restore_tool_link, backup_job_list, backup_job_create, backup_job_edit,
#    backup_job_test)
#from .literals import BACKUP_JOB_QUEUE_NAME
#from .models import App
#from . import models

#class UnableToRegister(Exception):
#    pass
        
#apipkg.initpkg(__name__, {
#    #'App': _App,
##    'App': 'app_registry.models:App',
#    #'App': models.App
#})
#pp = 1
#from .models import App#as _App#, BackupJob as _BackupJob

#@transaction.commit_on_success
#def create_backups_job_queue():
#    global backups_job_queue
#    try:
#        backups_job_queue, created = JobQueue.objects.get_or_create(name=BACKUP_JOB_QUEUE_NAME, defaults={'label': _('Backups'), 'unique_jobs': True})
#    except DatabaseError:
#        transaction.rollback()


#bind_links(['app_list'], [app_list], menu_name='secondary_menu')

#create_backups_job_queue()
###backup_job_type = JobType('remote_backup', _(u'Remove backup'), do_backup)

#register_setup(backup_tool_link)
#register_tool(restore_tool_link)
#bind_links([BackupJob, 'backup_job_list', 'backup_job_create'], [backup_job_list], menu_name='secondary_menu')
#bind_links([BackupJob, 'backup_job_list', 'backup_job_create'], [backup_job_create], menu_name='sidebar')
#bind_links([BackupJob], [backup_job_edit, backup_job_test])

#register_model_list_columns(BackupJob, [
#    {'name':_(u'begin date time'), 'attribute': 'begin_datetime'},
#    {'name':_(u'storage module'), 'attribute': 'storage_module.label'},
#    {'name':_(u'apps'), 'attribute': encapsulate(lambda x: u', '.join([unicode(app) for app in x.apps.all()]))},
#])

###app.set_backup([ModelBackup()])
