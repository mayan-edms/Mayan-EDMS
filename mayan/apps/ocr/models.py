from __future__ import absolute_import

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from .exceptions import ReQueueError
from .literals import (DOCUMENTQUEUE_STATE_CHOICES,
    QUEUEDOCUMENT_STATE_PENDING, QUEUEDOCUMENT_STATE_CHOICES,
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_ACTIVE)
from .managers import DocumentQueueManager


class DocumentQueue(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_(u'name'))
    label = models.CharField(max_length=64, verbose_name=_(u'label'))
    state = models.CharField(max_length=4,
        choices=DOCUMENTQUEUE_STATE_CHOICES,
        default=DOCUMENTQUEUE_STATE_ACTIVE,
        verbose_name=_(u'state'))

    objects = DocumentQueueManager()

    class Meta:
        verbose_name = _(u'document queue')
        verbose_name_plural = _(u'document queues')

    def __unicode__(self):
        return self.label


class QueueDocument(models.Model):
    document_queue = models.ForeignKey(DocumentQueue, verbose_name=_(u'document queue'))
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    datetime_submitted = models.DateTimeField(verbose_name=_(u'date time submitted'), auto_now_add=True, db_index=True)
    delay = models.BooleanField(verbose_name=_(u'delay ocr'), default=False)
    state = models.CharField(max_length=4,
        choices=QUEUEDOCUMENT_STATE_CHOICES,
        default=QUEUEDOCUMENT_STATE_PENDING,
        verbose_name=_(u'state'))
    result = models.TextField(blank=True, null=True, verbose_name=_(u'result'))
    node_name = models.CharField(max_length=32, verbose_name=_(u'node name'), blank=True, null=True)

    class Meta:
        ordering = ('datetime_submitted',)
        verbose_name = _(u'queue document')
        verbose_name_plural = _(u'queue documents')

    def requeue(self):
        if self.state == QUEUEDOCUMENT_STATE_PROCESSING:
            raise ReQueueError
        else:
            self.datetime_submitted = now()
            self.state = QUEUEDOCUMENT_STATE_PENDING
            self.delay = False
            self.result = None
            self.node_name = None
            self.save()

    def __unicode__(self):
        try:
            return unicode(self.document)
        except ObjectDoesNotExist:
            return ugettext(u'Missing document.')
