from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ClusterSetting(models.Model):
    """
    Define a setting entry common to all nodes in a cluster
    """
    name = models.CharField(unique=True, max_length=64, verbose_name=_(u'name'))
    value = models.TextField(blank=True, verbose_name=_(u'value'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'cluster setting')
        verbose_name_plural = _(u'cluster settings')
