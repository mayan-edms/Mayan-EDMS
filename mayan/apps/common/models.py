from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

SINGLETON_LOCK_ID = 1


class SingletonManager(models.Manager):
    def get(self, **kwargs):
        instance, created = self.model.objects.get_or_create(lock_id=SINGLETON_LOCK_ID, **kwargs)
        return instance


class Singleton(models.Model):
    lock_id = models.CharField(max_length=1, default=SINGLETON_LOCK_ID, editable=False, verbose_name=_(u'lock field'), unique=True)

    objects = SingletonManager()

    def save(self, *args, **kwargs):
        self.id = 1
        super(Singleton, self).save(*args, **kwargs)

    def delete(self, force=False, *args, **kwargs):
        if force:
            return super(Singleton, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class AnonymousUserSingletonManager(SingletonManager):
    def passthru_check(self, user):
        if isinstance(user, AnonymousUser):
            return self.model.objects.get()
        else:
            return user


class AnonymousUserSingleton(Singleton):
    objects = AnonymousUserSingletonManager()

    def __unicode__(self):
        return ugettext('Anonymous user')

    class Meta:
        verbose_name = _(u'anonymous user')
        verbose_name_plural = _(u'anonymous user')


class AutoAdminSingleton(Singleton):
    account = models.ForeignKey(User, null=True, blank=True, related_name='auto_admin_account', verbose_name=_(u'account'))
    password = models.CharField(null=True, blank=True, verbose_name=_(u'password'), max_length=128)
    password_hash = models.CharField(null=True, blank=True, verbose_name=_(u'password hash'), max_length=128)

    class Meta:
        verbose_name = verbose_name_plural = _(u'auto admin properties')
