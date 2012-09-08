from __future__ import absolute_import

import inspect
#import runpy

from django.conf import settings
from django.db import transaction, DatabaseError
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from .models import App

#from navigation.api import bind_links, register_model_list_columns

#from .links import (app_registry_tool_link, app_list, backup_tool_link, 
#    restore_tool_link, backup_job_list, backup_job_create, backup_job_edit,
#    backup_job_test)

#bind_links(['app_list'], [app_list], menu_name='secondary_menu')
###app.set_backup([ModelBackup()])

for app_name in settings.INSTALLED_APPS:
    App.register(app_name)
    print 'registry', app_name
        
    try:
        post_init = import_module('%s.post_init' % app_name)
    except ImportError:
        pass
    else:
        print 'post', post_init
        if post_init:
            for name, value in inspect.getmembers(post_init):
                if hasattr(value, '__call__') and name.startswith('init'):
                    value()
