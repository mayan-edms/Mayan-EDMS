from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BootstrapSetup(models.Model):
    """
    Model to store the fixture for a pre configured setup
    """
    name = models.CharField(max_length=128, verbose_name=_(u'name'), unique=True)
    description = models.TextField(verbose_name=_(u'description'), blank=True)
    fixture = models.TextField(verbose_name=_(u'fixture'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'bootstrap setup')
        verbose_name_plural = _(u'bootstrap setups')
