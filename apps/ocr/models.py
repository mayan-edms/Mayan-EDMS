from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from literals import DOCUMENTQUEUE_STATE_STOPPED,\
    DOCUMENTQUEUE_STATE_CHOICES, QUEUEDOCUMENT_STATE_PENDING,\
    QUEUEDOCUMENT_STATE_CHOICES


def add_document_to_queue(document, queue_name='default'):
    document_queue = DocumentQueue.objects.get(name=queue_name)
    queue_document = QueueDocument(document_queue=document_queue, document=document)
    queue_document.save()
    return document_queue
    

class DocumentQueue(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_(u'name'))
    label = models.CharField(max_length=64, verbose_name=_(u'label'))
    state = models.CharField(max_length=4,
        choices=DOCUMENTQUEUE_STATE_CHOICES,
        default=DOCUMENTQUEUE_STATE_STOPPED,
        verbose_name=_(u'state'))
    
    class Meta:
        verbose_name = _(u'document queue')
        verbose_name_plural = _(u'document queues')

    def __unicode__(self):
        return self.label

    def add_document(self, document):
        queue_document = QueueDocument(document_queue=self, document=document)
        queue_document.save()
        

class QueueDocument(models.Model):
    document_queue = models.ForeignKey(DocumentQueue, verbose_name=_(u'document queue'))
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    datetime_submitted = models.DateTimeField(verbose_name=_(u'date time submitted'), auto_now_add=True)
    state = models.CharField(max_length=4,
        choices=QUEUEDOCUMENT_STATE_CHOICES,
        default=QUEUEDOCUMENT_STATE_PENDING,
        verbose_name=_(u'state'))
    result = models.TextField(blank=True, null=True, verbose_name=_(u'result'))
    
    class Meta:
        ordering = ('datetime_submitted',)
        verbose_name = _(u'queue document')
        verbose_name_plural = _(u'queue documents')

    def __unicode__(self):
        return unicode(self.document)
