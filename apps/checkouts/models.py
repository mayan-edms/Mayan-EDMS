from __future__ import absolute_import

import logging
import datetime

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from documents.models import Document
from history.api import create_history

from .managers import DocumentCheckoutManager
from .exceptions import DocumentAlreadyCheckedOut
from .events import HISTORY_DOCUMENT_CHECKED_OUT

logger = logging.getLogger(__name__)


class DocumentCheckout(models.Model):
    """
    Model to store the state and information of a document checkout
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'), unique=True)
    checkout_datetime = models.DateTimeField(verbose_name=_(u'check out date and time'), blank=True, null=True)
    expiration_datetime = models.DateTimeField(verbose_name=_(u'check out expiration date and time'), help_text=_(u'Amount of time to hold the document checked out in minutes.'))
    user_content_type = models.ForeignKey(ContentType, null=True, blank=True)  # blank and null added for ease of db migration
    user_object_id = models.PositiveIntegerField(null=True, blank=True)
    user_object = generic.GenericForeignKey(ct_field='user_content_type', fk_field='user_object_id')

    block_new_version = models.BooleanField(default=True, verbose_name=_(u'block new version upload'), help_text=_(u'Do not allow new version of this document to be uploaded.'))

    #block_metadata
    #block_editing
    #block tag add/remove
    
    objects = DocumentCheckoutManager()
    
    def __unicode__(self):
        return unicode(self.document)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.checkout_datetime = datetime.datetime.now()
        result = super(DocumentCheckout, self).save(*args, **kwargs)
        create_history(HISTORY_DOCUMENT_CHECKED_OUT, source_object=self.document, data={'user': self.user_object, 'document': self.document})
        return result
    
    @models.permalink
    def get_absolute_url(self):
        return ('checkout_info', [self.document.pk])        
        
    class Meta:
        verbose_name = _(u'document checkout')
        verbose_name_plural = _(u'document checkouts')
