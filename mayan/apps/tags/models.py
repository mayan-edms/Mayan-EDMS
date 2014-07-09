from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag

from .literals import COLOR_CHOICES, COLOR_CODES


class TagProperties(models.Model):
    # TODO: this should be a One to One relation not a ForeignKey
    tag = models.ForeignKey(Tag, verbose_name=_(u'tag'), related_name='properties')
    color = models.CharField(max_length=3, choices=COLOR_CHOICES, verbose_name=_(u'color'))

    class Meta:
        verbose_name = _(u'tag properties')
        verbose_name_plural = _(u'tags properties')

    def __unicode__(self):
        return unicode(self.tag)

    def get_color_code(self):
        return dict(COLOR_CODES)[self.color]
