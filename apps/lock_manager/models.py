from __future__ import absolute_import

import datetime

from django.db import close_connection
from django.db import (models, transaction, DatabaseError)
from django.utils.translation import ugettext_lazy as _

from .managers import LockManager
#from .settings import DEFAULT_LOCK_TIMEOUT
DEFAULT_LOCK_TIMEOUT = 60

class Lock(models.Model):
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'))
    timeout = models.IntegerField(default=DEFAULT_LOCK_TIMEOUT, verbose_name=_(u'timeout'))
    name = models.CharField(max_length=48, verbose_name=_(u'name'), unique=True)

    objects = LockManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.creation_datetime = datetime.datetime.now()
        if not self.timeout and not kwargs.get('timeout'):
            self.timeout = DEFAULT_LOCK_TIMEOUT

        super(Lock, self).save(*args, **kwargs)

    @transaction.commit_on_success
    def release(self):
        try:
            close_connection()
            lock = Lock.objects.get(name=self.name, creation_datetime=self.creation_datetime)
            lock.delete()
        except Lock.DoesNotExist:
            # Lock expired and was reassigned
            pass
        except DatabaseError:
            transaction.rollback()
        finally:
            close_connection()

    class Meta:
        verbose_name = _(u'lock')
        verbose_name_plural = _(u'locks')
