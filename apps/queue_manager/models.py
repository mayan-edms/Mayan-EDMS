from __future__ import absolute_import

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.simplejson import loads, dumps
from django.db import IntegrityError

from .exceptions import QueuePushError

queue_labels = {}


class QueueManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        queue_labels[kwargs.get('name')] = kwargs.get('defaults', {}).get('label')
        return super(QueueManager, self).get_or_create(*args, **kwargs)


class Queue(models.Model):
    # Internal name
    name = models.CharField(max_length=32, verbose_name=_(u'name'), unique=True)
    unique_names = models.BooleanField(verbose_name=_(u'unique names'), default=False)

    objects = QueueManager()

    def __unicode__(self):
        return unicode(self.label) or self.name
        
    @property
    def label(self):
        return queue_labels.get(self.name)

    def push(self, data, name=None):  # TODO: add replace flag
        if not name:
            name = u''
        queue_item = QueueItem(queue=self, name=name, data=dumps(data))
        queue_item.save()
        return queue_item
        
    def pull(self):
        queue_item_qs = QueueItem.objects.filter(queue=self).order_by('-creation_datetime')
        if queue_item_qs:
            queue_item = queue_item_qs[0]
            queue_item.delete()
            return loads(queue_item.data)
        
    @property
    def items(self):
        return self.queueitem_set
        
    def empty(self):
        self.items.all().delete()
        
    def save(self, *args, **kwargs):
        label = getattr(self, 'label', None)
        if label:
            queue_labels[self.name] = label
        return super(Queue, self).save(*args, **kwargs)
        
    # TODO: custom runtime methods
        
    class Meta:
        verbose_name = _(u'queue')
        verbose_name_plural = _(u'queues')


class QueueItem(models.Model):
    queue = models.ForeignKey(Queue, verbose_name=_(u'queue'))
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'), editable=False)
    unique_name = models.CharField(blank=True, max_length=32, verbose_name=_(u'name'), unique=True, editable=False)
    name = models.CharField(blank=True, max_length=32, verbose_name=_(u'name'))
    data = models.TextField(verbose_name=_(u'data'))
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.creation_datetime = datetime.now()

        if self.queue.unique_names:
            self.unique_name = self.name
        else:
            self.unique_name = unicode(self.creation_datetime)
        try:
            super(QueueItem, self).save(*args, **kwargs)
        except IntegrityError:
            # TODO: Maybe replace instead or rasining exception w/ replace flag
            raise QueuePushError
    
    class Meta:
        verbose_name = _(u'queue item')
        verbose_name_plural = _(u'queue items')
    
