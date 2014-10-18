from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from .literals import COLOR_CHOICES, COLOR_CODES


class Tag(models.Model):
    label = models.CharField(max_length=128, verbose_name=_(u'Label'), unique=True, db_index=True)
    color = models.CharField(max_length=3, choices=COLOR_CHOICES, verbose_name=_(u'Color'))
    documents = models.ManyToManyField(Document, related_name='tags', verbose_name=_('Documents'))

    class Meta:
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')

    def __unicode__(self):
        return self.label

    def get_color_code(self):
        return dict(COLOR_CODES)[self.color]
