from __future__ import absolute_import

import datetime
import logging
import imp
import sys

from django.db import models
from django.db import DatabaseError, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.importlib import import_module

from common.models import TranslatableLabelMixin, LiveObjectMixin
from smart_settings import SettingsNamespace
from project_setup.api import register_setup
from project_tools.api import register_tool

#from .classes import AppBackup, StorageModuleBase, Setting

logger = logging.getLogger(__name__)


class App(TranslatableLabelMixin, LiveObjectMixin, models.Model):
    translatables = ['label', 'description', 'icon']

    #class UnableToRegister(Exception):
    #    pass
    
    name = models.CharField(max_length=64, verbose_name=_(u'name'), unique=True)
    dependencies = models.ManyToManyField('self', verbose_name=_(u'dependencies'), symmetrical=False, blank=True, null=True)
    #version
    #top_urls
    #namespace

    @classmethod
    @transaction.commit_on_success
    def register(cls, app_name):
        try:
            app_module = import_module(app_name)
        except ImportError:
            transaction.rollback
        else:
            try:
                registration = import_module('%s.registry' % app_name)
            except ImportError:
                transaction.rollback
            else:
                disabled = getattr(registration, 'disabled', False)
                name = getattr(registration, 'name')
                label = getattr(registration, 'label')
                icon = getattr(registration, 'icon', None)
                description = getattr(registration, 'description', None)
                dependencies = getattr(registration, 'dependencies', [])
                settings = getattr(registration, 'settings', None)
                setup_links = getattr(registration, 'setup_links', [])
                tool_links = getattr(registration, 'tool_links', [])

                if not disabled:
                    try:
                        app, created = App.objects.get_or_create(name=name)
                    except DatabaseError:
                        transaction.rollback()
                        raise cls.UnableToRegister
                    else:
                        app.label = label
                        if description:
                            app.description = description
                        app.dependencies.clear()
                        app.save()
                        app.icon = icon

                        for app_name in dependencies:
                            dependency = App.objects.get(name=app_name)
                            app.dependencies.add(dependency)

                        if settings:
                            settings_module = imp.new_module('settings')
                            setattr(app_module, 'settings', settings_module)
                            sys.modules['%s.settings' % name] = settings_module 
                            settings_namespace = SettingsNamespace(name, label, '%s.settings' % name)
                            for setting in settings:
                                settings_namespace.add_setting(**setting)
                        
                        for link in setup_links:
                            register_setup(link) 

                        for link in tool_links:
                            register_tool(link)
           
    #def set_backup(self, *args, **kwargs):
    #    return AppBackup(self, *args, **kwargs)
       
    def __unicode__(self):
        return unicode(self.label)

    class Meta:
        ordering = ('name', )
        verbose_name = _(u'app')
        verbose_name_plural = _(u'apps')


