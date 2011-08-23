import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lock_manager.managers import LockManager
from lock_manager.conf.settings import DEFAULT_LOCK_TIMEOUT


class Lock(models.Model):
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'))
    timeout = models.IntegerField(default=DEFAULT_LOCK_TIMEOUT, verbose_name=_(u'timeout'))
    name = models.CharField(max_length=32, verbose_name=_(u'name'), unique=True)
    
    objects = LockManager()
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.creation_datetime = datetime.datetime.now()
        super(Lock, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = _(u'lock')
        verbose_name_plural = _(u'locks')
