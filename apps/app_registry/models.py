from __future__ import absolute_import

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

logger = logging.getLogger(__name__)


class TranslatableLabelMixin(models.Model):
    _labels = {}
    
    @property
    def label(self):
        try:
            return self.__class__._labels[self.pk]
        except KeyError:
            return unicode(self.__class__)

    def __setattr__(self, attr, value):
        if attr == 'label':
            self.__class__._labels[self.pk] = value
        else:
            return super(TranslatableLabelMixin, self).__setattr__(attr, value)
    
    def __unicode__(self):
        return unicode(self.label)

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


class App(TranslatableLabelMixin, LiveObjectMixin, models.Model):
    name = models.CharField(max_length=64, verbose_name=_(u'name'), unique=True)
    icon = models.CharField(max_length=64, verbose_name=_(u'icon'), blank=True)

    class Meta:
        ordering = ('name', )
        verbose_name = _(u'app')
        verbose_name_plural = _(u'apps')
