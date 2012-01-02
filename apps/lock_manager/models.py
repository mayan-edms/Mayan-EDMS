from __future__ import absolute_import

import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import LockManager
from .conf.settings import DEFAULT_LOCK_TIMEOUT


class Lock(models.Model):
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'))
    timeout = models.IntegerField(default=DEFAULT_LOCK_TIMEOUT, verbose_name=_(u'timeout'))
    name = models.CharField(max_length=48, verbose_name=_(u'name'), unique=True)

    objects = LockManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.creation_datetime = datetime.datetime.now()
        if not self.timeout and not kwarget.get('timeout'):
            self.timeout = DEFAULT_LOCK_TIMEOUT

        super(Lock, self).save(*args, **kwargs)

    def release(self):
        try:
            lock = Lock.objects.get(name=self.name, creation_datetime=self.creation_datetime)
            lock.delete()
        except Lock.DoesNotExist:
            # Out lock expired and was reassigned
            pass

    class Meta:
        verbose_name = _(u'lock')
        verbose_name_plural = _(u'locks')
