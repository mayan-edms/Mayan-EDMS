from __future__ import absolute_import

from ast import literal_eval
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ValidationError

from documents.models import Document
from converter.api import get_available_transformations_choices
from sources.managers import SourceTransformationManager

from .literals import (DOCUMENTQUEUE_STATE_STOPPED,
    DOCUMENTQUEUE_STATE_CHOICES, QUEUEDOCUMENT_STATE_PENDING,
    QUEUEDOCUMENT_STATE_CHOICES, QUEUEDOCUMENT_STATE_PROCESSING,
    DOCUMENTQUEUE_STATE_ACTIVE)
from .managers import DocumentQueueManager
from .exceptions import ReQueueError


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

    def get_transformation_list(self):
        return QueueTransformation.transformations.get_for_object_as_list(self)

    def requeue(self):
        if self.state == QUEUEDOCUMENT_STATE_PROCESSING:
            raise ReQueueError
        else:
            self.datetime_submitted = datetime.now()
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


class ArgumentsValidator(object):
    message = _(u'Enter a valid value.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        '''
        Validates that the input evaluates correctly.
        '''
        value = value.strip()
        try:
            literal_eval(value)
        except (ValueError, SyntaxError):
            raise ValidationError(self.message, code=self.code)


class QueueTransformation(models.Model):
    '''
    Model that stores the transformation and transformation arguments
    for a given document queue
    '''
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_(u'order'), db_index=True)
    transformation = models.CharField(choices=get_available_transformations_choices(), max_length=128, verbose_name=_(u'transformation'))
    arguments = models.TextField(blank=True, null=True, verbose_name=_(u'arguments'), help_text=_(u'Use dictionaries to indentify arguments, example: %s') % u'{\'degrees\':90}', validators=[ArgumentsValidator()])

    objects = models.Manager()
    transformations = SourceTransformationManager()

    def __unicode__(self):
        return self.get_transformation_display()

    class Meta:
        ordering = ('order',)
        verbose_name = _(u'document queue transformation')
        verbose_name_plural = _(u'document queue transformations')
