from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import LockManager
from .settings import DEFAULT_LOCK_TIMEOUT


class Lock(models.Model):
    creation_datetime = models.DateTimeField(verbose_name=_('Creation datetime'), auto_now_add=True)
    timeout = models.IntegerField(default=DEFAULT_LOCK_TIMEOUT, verbose_name=_('Timeout'))
    name = models.CharField(max_length=48, verbose_name=_('Name'), unique=True)

    objects = LockManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.timeout and not kwargs.get('timeout'):
            self.timeout = DEFAULT_LOCK_TIMEOUT

        super(Lock, self).save(*args, **kwargs)

    def release(self):
        try:
            lock = Lock.objects.get(name=self.name, creation_datetime=self.creation_datetime)
        except Lock.DoesNotExist:
            # Our lock has expired and was reassigned
            pass
        else:
            lock.delete()

    class Meta:
        verbose_name = _('Lock')
        verbose_name_plural = _('Locks')
