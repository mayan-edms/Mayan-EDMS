from __future__ import absolute_import

import os
import datetime
import platform

import psutil

from django.db import models, IntegrityError, transaction
from django.db import close_connection
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


class NodeManager(models.Manager):
    def myself(self):
        node, created = self.model.objects.get_or_create(hostname=platform.node(), defaults={'memory_usage': 100})
        node.refresh()
        return node


class Node(models.Model):
    hostname = models.CharField(max_length=255, verbose_name=_(u'hostname'))
    cpuload = models.PositiveIntegerField(blank=True, default=0, verbose_name=_(u'cpu load'))
    heartbeat = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name=_(u'last heartbeat check'))
    memory_usage = models.FloatField(blank=True, verbose_name=_(u'memory usage'))
    
    objects = NodeManager()

    def __unicode__(self):
        return self.hostname
        
    def refresh(self):
        self.cpuload = psutil.cpu_percent()
        self.memory_usage = psutil.phymem_usage().percent
        self.save()
   
    def save(self, *args, **kwargs):
        self.heartbeat = datetime.datetime.now()
        return super(Node, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'node')
        verbose_name_plural = _(u'nodes')
