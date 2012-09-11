from django.db import models

from app_registry.models import App

"""
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
"""
