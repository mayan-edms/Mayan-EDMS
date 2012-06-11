from __future__ import absolute_import

import logging
import datetime

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from .managers import DocumentCheckoutManager
from .exceptions import DocumentAlreadyCheckedOut

logger = logging.getLogger(__name__)


class DocumentCheckout(models.Model):
    """
    Model to store the state and information of a document checkout
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'), unique=True, editable=False)
    checkout_datetime = models.DateTimeField(verbose_name=_(u'checkout date and time'), editable=False)
    expiration_datetime = models.DateTimeField(verbose_name=_(u'checkout expiration date and time'))
    block_new_version = models.BooleanField(verbose_name=_(u'block new version upload'), help_text=_(u'Do not allow new version of this document to be uploaded.'))
    #block_metadata
    #block_editing
    #block tag add/remove
    
    objects = DocumentCheckoutManager()
    
    def __unicode__(self):
        return unicode(self.document)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.checkout_date = datetime.datetime.now()
        try:
            return super(DocumentCheckout, self).save(*args, **kwargs)
        except IntegrityError:
            raise DocumentAlreadyCheckedOut
    
    @models.permalink
    def get_absolute_url(self):
        return ('checkout_info', [self.document.pk])        
        
    class Meta:
        verbose_name = _(u'document checkout')
        verbose_name_plural = _(u'document checkouts')
