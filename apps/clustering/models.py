from __future__ import absolute_import

import os
import datetime
import platform

import psutil

from django.db import models, IntegrityError, transaction
from django.db import close_connection
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from common.models import Singleton

DEFAULT_NODE_TTL = 5
DEFAULT_NODE_HEARTBEAT_INTERVAL = 1


class NodeManager(models.Manager):
    def myself(self):
        node, created = self.model.objects.get_or_create(hostname=platform.node())
        node.refresh()
        if created:
            # Store the refresh data because is a new instance
            node.save()
        return node


class Node(models.Model):
    hostname = models.CharField(max_length=255, verbose_name=_(u'hostname'))
    cpuload = models.FloatField(blank=True, default=0.0, verbose_name=_(u'cpu load'))
    heartbeat = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name=_(u'last heartbeat check'))
    memory_usage = models.FloatField(blank=True, default=0.0, verbose_name=_(u'memory usage'))

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
            # Make we can only update ourselves
            info = Node.platform_info()
            self.cpuload = info['cpuload']
            self.memory_usage = info['memory_usage']
        
    def save(self, *args, **kwargs):
        self.heartbeat = datetime.datetime.now()
        return super(Node, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'node')
        verbose_name_plural = _(u'nodes')


class ClusteringConfigManager(models.Manager):
    def dead_nodes(self):
        return Node.objects.filter(heartbeat__lt=datetime.datetime.now() - datetime.timedelta(seconds=self.model.get().node_time_to_live))

    def delete_dead_nodes(self):
        self.dead_nodes().delete()

    def zombiest_node(self):
        try:
            return self.dead_nodes().order_by('-heartbeat')[0]
        except IndexError:
            return None


class ClusteringConfig(Singleton):
    node_time_to_live = models.PositiveIntegerField(verbose_name=(u'time to live (in seconds)'), default=DEFAULT_NODE_TTL) #  After this time a worker is considered dead
    node_heartbeat_interval = models.PositiveIntegerField(verbose_name=(u'heartbeat interval'), default=DEFAULT_NODE_HEARTBEAT_INTERVAL)
    # TODO: add validation, interval cannot be greater than TTL

    objects = ClusteringConfigManager()

    def __unicode__(self):
        return ugettext('clustering config')

    class Meta:
        verbose_name = verbose_name_plural = _(u'clustering config')
