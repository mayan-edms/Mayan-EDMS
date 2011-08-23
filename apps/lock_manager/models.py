import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.utils import IntegrityError
from django.db import transaction


class LockError(Exception):
    pass

class LockManager(models.Manager):
    @transaction.commit_manually
    def acquire_lock(self, name):
        lock = self.model(name=name)
        try:
            lock.save(force_insert=True)
        except IntegrityError:
            transaction.rollback()
            # There is already an existing lock
            # Check it's expiration date and if expired delete it and 
            # re-create it
            lock = Lock.objects.get(name=name)
            if datetime.datetime.now() > lock.creation_datetime + datetime.timedelta(seconds=lock.expiration):
                release_lock(self)
                lock.save()
            else:
                raise LockError('Unable to acquire lock')
        else:
            transaction.commit()
        
    @transaction.commit_manually
    def release_lock(self, name):
        lock = Lock.objects.get(name=name)
        lock.delete()
        transaction.commit()

class Lock(models.Model):
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'))
    expiration_time = models.IntegerField(default=3600, verbose_name=_(u'expiration time'))
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
