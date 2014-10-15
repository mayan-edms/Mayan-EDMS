from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType


class DocumentTypeStateCollection(models.Model):
    document_type = models.ForeignKey(DocumentType, related_name='state_collections', verbose_name=_('Document type'))
    label = models.CharField(max_length=128, verbose_name=_('Label'))

    class Meta:
        verbose_name = _('Document type state collection')
        verbose_name_plural = _('Document type state collections')

    def __unicode__(self):
        return self.label


class State(models.Model):
    document_type_state_collection = models.ForeignKey(DocumentTypeStateCollection, related_name='states', verbose_name=_('Document type state collection'))
    label = models.CharField(max_length=128, verbose_name=_('Label'))
    initial = models.BooleanField(default=False, verbose_name=_('Initial'))

    class Meta:
        verbose_name = _('State template')
        verbose_name_plural = _('State templates')

    def __unicode__(self):
        return self.label


class StateTransition(models.Model):
    source_state_template = models.ForeignKey(State, related_name='transitions', verbose_name=_('Source state'))
    destination_state_template = models.ForeignKey(State, verbose_name=_('Destination state'))

    class Meta:
        verbose_name = _('State transition')
        verbose_name_plural = _('State transitions')

    def __unicode__(self):
        return u'{} => {}'.format(self.source_state_template, self.destination_state_template)


class DocumentStateLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Date time'))
    document = models.ForeignKey(Document, related_name='states_log', verbose_name=_('Document'))
    document_type_state_collection = models.ForeignKey(DocumentTypeStateCollection, verbose_name=_('Document type state collection'))
    state = models.ForeignKey(State, verbose_name=_('State'))

    class Meta:
        unique_together = ('document', 'document_type_state_collection')
        verbose_name = _('Document state log')
        verbose_name_plural = _(u'Document state logs')

    def __unicode__(self):
        return self.state
