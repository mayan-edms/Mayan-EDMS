from __future__ import absolute_import

import logging
import imp
import sys

from django.db import models
from django.db import DatabaseError, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from common.models import TranslatableLabelMixin, LiveObjectMixin
from smart_settings import SettingsNamespace
from project_setup.api import register_setup
from project_tools.api import register_tool
from statistics.api import register_statistics
from navigation.api import register_top_menu
from bootstrap.classes import Cleanup, BootstrapModel

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
        logger.debug('Trying to import: %s' % app_name)
        try:
            app_module = import_module(app_name)
        except ImportError:
            transaction.rollback
            logger.debug('Unable to import app: %s' % app_name)
        else:
            logger.debug('Trying to import registry from: %s' % app_name)
            try:
                registration = import_module('%s.registry' % app_name)
            except ImportError:
                transaction.rollback
                logger.debug('Unable to import registry for app: %s' % app_name)
            else:
                if not getattr(registration, 'disabled', False):
                    try:
                        app, created = App.objects.get_or_create(name=app_name)
                    except DatabaseError:
                        transaction.rollback()
                        # If database is not ready create a memory only app instance
                        app = App()
                        app.label = getattr(registration, 'label', app_name)
                        app.description = getattr(registration, 'description', u'')
                    else:
                        # If there are not error go ahead with the stored app instance
                        app.label = getattr(registration, 'label', app_name)
                        app.description = getattr(registration, 'description', u'')
                        app.dependencies.clear()
                        app.save()
                        for dependency_name in getattr(registration, 'dependencies', []):
                            dependency, created = App.objects.get_or_create(name=dependency_name)
                            app.dependencies.add(dependency)

                    app.icon = getattr(registration, 'icon', None)
                    settings = getattr(registration, 'settings', None)

                    if settings:
                        logger.debug('settings: %s' % settings)
                        settings_module = imp.new_module('settings')
                        setattr(app_module, 'settings', settings_module)
                        sys.modules['%s.settings' % app_name] = settings_module 
                        settings_namespace = SettingsNamespace(app_name, app.label, '%s.settings' % app_name)
                        for setting in settings:
                            settings_namespace.add_setting(**setting)
                          
                    for link in getattr(registration, 'setup_links', []):
                        logger.debug('setup link: %s' % link)
                        register_setup(link) 

                    for link in getattr(registration, 'tool_links', []):
                        logger.debug('tool link: %s' % link)
                        register_tool(link)
                        
                    for statistic in getattr(registration, 'statistics', []):
                        logger.debug('statistic: %s' % statistic)
                        register_statistics(statistic)
                    
                    for index, link in enumerate(getattr(registration, 'menu_links', [])):
                        logger.debug('menu_link: %s' % link)
                        register_top_menu(name='%s.%s' % (app_name, index), link=link)

                    for cleanup_function in getattr(registration, 'cleanup_functions', []):
                        logger.debug('cleanup_function: %s' % cleanup_function)
                        Cleanup(cleanup_function)

                    for bootstrap_model in getattr(registration, 'bootstrap_models', []):
                        logger.debug('bootstrap_model: %s' % bootstrap_model)
                        BootstrapModel(model_name=bootstrap_model.get('name'), app_name=app_name, sanitize=bootstrap_model.get('sanitize', True), dependencies=bootstrap_model.get('dependencies'))

    def __unicode__(self):
        return unicode(self.label)

    class Meta:
        ordering = ('name', )
        verbose_name = _(u'app')
        verbose_name_plural = _(u'apps')
