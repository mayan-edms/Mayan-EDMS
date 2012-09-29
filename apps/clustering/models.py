from __future__ import absolute_import

import os
import datetime
import platform

import psutil

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from common.models import Singleton

from .literals import (DEFAULT_NODE_HEARTBEAT_INTERVAL, DEFAULT_NODE_HEARTBEAT_TIMEOUT,
    DEFAULT_DEAD_NODE_REMOVAL_INTERVAL, NODE_STATE_HEALTHY, NODE_STATE_CHOICES, NODE_STATE_DEAD,
    DEFAULT_NODE_CPU_LOAD, DEFAULT_NODE_MEMORY_USAGE)
from .signals import node_died


class NodeManager(models.Manager):
    def myself(self):
        node, created = self.model.objects.get_or_create(hostname=platform.node())
        node.refresh()
        if created:
            # Store the refresh data because is a new instance
            node.save()
        return node

    def live_nodes(self):
        return self.model.objects.filter(state=NODE_STATE_HEALTHY)

    def dead_nodes(self):
        from .literals import DEFAULT_NODE_HEARTBEAT_TIMEOUT
        return self.model.objects.filter(state=NODE_STATE_HEALTHY).filter(heartbeat__lt=datetime.datetime.now() - datetime.timedelta(seconds=DEFAULT_NODE_HEARTBEAT_TIMEOUT))

    def check_dead_nodes(self):
        for node in self.dead_nodes():
            node.mark_as_dead()


class Node(models.Model):
    hostname = models.CharField(max_length=255, verbose_name=_(u'hostname'), unique=True)
    cpuload = models.FloatField(blank=True, default=DEFAULT_NODE_CPU_LOAD, verbose_name=_(u'cpu load'))
    heartbeat = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name=_(u'last heartbeat check'))
    memory_usage = models.FloatField(blank=True, default=DEFAULT_NODE_MEMORY_USAGE, verbose_name=_(u'memory usage'))
    state = models.CharField(max_length=4,
        choices=NODE_STATE_CHOICES,
        default=NODE_STATE_DEAD,
        verbose_name=_(u'state'))
        
    objects = NodeManager()
    
    @classmethod
    def platform_info(cls):
        return {
            'cpuload': psutil.cpu_percent(),
            'memory_usage': psutil.phymem_usage().percent
        }
    
    def __unicode__(self):
        return self.hostname
        
    def refresh(self):
        if self.hostname == platform.node():
            # Make sure we can only update ourselves
            info = Node.platform_info()
            self.cpuload = info['cpuload']
            self.memory_usage = info['memory_usage']

    def is_healthy(self):
        return self.state == NODE_STATE_HEALTHY
        
    def mark_as_dead(self):
        self.state = NODE_STATE_DEAD
        node_died.send(sender=self, node=self)
        self.save()
        
    def send_heartbeat(self):
        self.refresh()
        self.state = NODE_STATE_HEALTHY
        self.heartbeat = datetime.datetime.now()
        self.save()

    class Meta:
        verbose_name = _(u'node')
        verbose_name_plural = _(u'nodes')
