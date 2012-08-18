from __future__ import absolute_import

import datetime
import logging

from django.db import models
from django.db import DatabaseError, transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from common.models import TranslatableLabelMixin, LiveObjectMixin

from .classes import AppBackup, StorageModuleBase

logger = logging.getLogger(__name__)


class App(TranslatableLabelMixin, LiveObjectMixin, models.Model):
    translatables = ['label', 'description']

    class UnableToRegister(Exception):
        pass
    
    name = models.CharField(max_length=64, verbose_name=_(u'name'), unique=True)
    icon = models.CharField(max_length=64, verbose_name=_(u'icon'), blank=True)
    dependencies = models.ManyToManyField('self', verbose_name=_(u'dependencies'), symmetrical=False, blank=True, null=True)
    #version
    #top_urls
    #namespace

    @classmethod
    @transaction.commit_on_success
    def register(cls, name, label, icon=None, description=None):
        try:
            app, created = App.objects.get_or_create(name=name)
        except DatabaseError:
            transaction.rollback()
            raise UnableToRegister
        else:
            app.label = label
            if icon:
                app.icon = icon
            if description:
                app.description = description
            app.dependencies.clear()
            app.save()
            return app    
    
    def set_dependencies(self, app_names):
        for app_name in app_names:
            app = App.objects.get(name=app_name)
            self.dependencies.add(app)
            
    def set_backup(self, *args, **kwargs):
        return AppBackup(self, *args, **kwargs)
        
    def __unicode__(self):
        return unicode(self.label)

    class Meta:
        ordering = ('name', )
        verbose_name = _(u'app')
        verbose_name_plural = _(u'apps')


class BackupJob(models.Model):
    name = models.CharField(max_length=64, verbose_name=_(u'name'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    apps = models.ManyToManyField(App)
    begin_datetime = models.DateTimeField(verbose_name=_(u'begin date and time'), default=lambda: datetime.datetime.now())

    # * repetition = 
    #   day - 1 days
    #    weekly - days of week checkbox
    #   month - day of month, day of week
    # * repetition option field
    # * ends
    #   - never
    #   - After # ocurrences
    #   - On date
    # * end option field
    # * type
    #    - Full
    #    - Incremental
    storage_module_name = models.CharField(max_length=32, choices=StorageModuleBase.get_as_choices(), verbose_name=_(u'storage module'))
    storage_arguments_json = models.TextField(verbose_name=_(u'storage module arguments (in JSON)'), blank=True)

    def __unicode__(self):
        return self.name

    @property
    def storage_module(self):
        return StorageModuleBase.get(self.storage_module_name)

    def backup(self, dry_run=False):
        logger.debug('starting: %s', self)
        logger.debug('dry_run: %s' % dry_run)
        storage_module = self.storage_module
        #TODO: loads
        for app in self.apps.all():
            app_backup = AppBackup.get(app)
            app_backup.backup(storage_module(backup_path='/tmp'), dry_run=dry_run)

    def save(self, *args, **kwargs):
        #dump
        super(BackupJob, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('checkout_info', [self.document.pk])

    class Meta:
        verbose_name = _(u'document checkout')
        verbose_name_plural = _(u'document checkouts')


#class BackupJobLog
