from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import SmartLinkManager
from .literals import (OPERATOR_CHOICES, INCLUSION_AND,
    INCLUSION_CHOICES)


class SmartLink(models.Model):
    title = models.CharField(max_length=96, verbose_name=_(u'Title'))
    dynamic_title = models.CharField(blank=True, max_length=96, verbose_name=_(u'Dynamic title'), help_text=_(u'This expression will be evaluated against the current selected document.  The document metadata is available as variables `metadata` and document properties under the variable `document`.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'Enabled'))

    objects = SmartLinkManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'Smart link')
        verbose_name_plural = _(u'Smart links')


class SmartLinkCondition(models.Model):
    smart_link = models.ForeignKey(SmartLink, verbose_name=_(u'Smart link'))
    inclusion = models.CharField(default=INCLUSION_AND, max_length=16, choices=INCLUSION_CHOICES, help_text=_(u'The inclusion is ignored for the first item.'))
    foreign_document_data = models.CharField(max_length=32, verbose_name=_(u'Foreign document data'), help_text=_(u'This represents the metadata of all other documents.  Available objects: `document.<attribute>` and `metadata.<metadata_type_name>`.'))
    operator = models.CharField(max_length=16, choices=OPERATOR_CHOICES)
    expression = models.TextField(verbose_name=_(u'Expression'), help_text=_(u'This expression will be evaluated against the current selected document.  The document metadata is available as variables `metadata` and document properties under the variable `document`.'))
    negated = models.BooleanField(default=False, verbose_name=_(u'Negated'), help_text=_(u'Inverts the logic of the operator.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'Enabled'))

    def __unicode__(self):
        return u'%s foreign %s %s %s %s' % (self.get_inclusion_display(), self.foreign_document_data, _(u'not') if self.negated else u'', self.get_operator_display(), self.expression)

    class Meta:
        verbose_name = _(u'Link condition')
        verbose_name_plural = _(u'Link conditions')
