from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User

SINGLETON_LOCK_ID = 1


class SingletonManager(models.Manager):
    def get(self, **kwargs):
        instance, created = self.model.singleton.get_or_create(lock_id=SINGLETON_LOCK_ID, **kwargs)
        return instance


class Singleton(models.Model):
    lock_id = models.CharField(max_length=1, default=SINGLETON_LOCK_ID, editable=False, verbose_name=_(u'lock field'), unique=True)

    singleton = SingletonManager()
    
    @classmethod
    def get(cls):
        return cls.singleton.get()
        
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


class TranslatableLabelMixin(models.Model):
    _translatable_registry = {}
    
    class NotConfigured(Exception):
        pass
    
    def __getattr__(self, attr):
        if attr in self.__class__.translatables:
            try:
                return self.__class__._translatable_registry[self.pk][attr]
            except KeyError:
                return u''
        else:
            raise AttributeError('\'%s\' object has no attribute \'%s\'' % (self.__class__, attr))

    def __setattr__(self, attr, value):
        if not hasattr(self.__class__, 'translatables'):
            raise self.__class__.NotConfigured('Must specify a list of translatable class attributes')
            
        if attr in self.__class__.translatables:
            self.__class__._translatable_registry.setdefault(self.pk, {})
            self.__class__._translatable_registry[self.pk][attr] = value
        else:
            return super(TranslatableLabelMixin, self).__setattr__(attr, value)

    def __init__(self, *args, **kwargs):
        super(TranslatableLabelMixin, self).__init__(*args, **kwargs)
        self.__class__._translatable_registry.setdefault(self.pk, {})
        
    class Meta:
        abstract = True


class LiveObjectsManager(models.Manager):
    def get_query_set(self):
        return super(LiveObjectsManager, self).get_query_set().filter(pk__in=(entry.pk for entry in self.model._registry))


class LiveObjectMixin(models.Model):
    _registry = []
   
    def save(self, *args, **kwargs):
        super(LiveObjectMixin, self).save(*args, **kwargs)
        self.__class__._registry.append(self)
        return self

    live = LiveObjectsManager()
    objects = models.Manager()
    
    class Meta:
        abstract = True
