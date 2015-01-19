from __future__ import unicode_literals

import logging

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from .events import event_document_check_out
from .exceptions import DocumentAlreadyCheckedOut
from .managers import DocumentCheckoutManager

logger = logging.getLogger(__name__)


class DocumentCheckout(models.Model):
    """
    Model to store the state and information of a document checkout
    """
    document = models.ForeignKey(Document, verbose_name=_('Document'), unique=True)
    checkout_datetime = models.DateTimeField(verbose_name=_('Check out date and time'), auto_now_add=True)
    expiration_datetime = models.DateTimeField(verbose_name=_('Check out expiration date and time'), help_text=_('Amount of time to hold the document checked out in minutes.'))

    # TODO: simplify user_object to an instance of User
    user_content_type = models.ForeignKey(ContentType, null=True, blank=True)  # blank and null added for ease of db migration
    user_object_id = models.PositiveIntegerField(null=True, blank=True)
    user_object = generic.GenericForeignKey(ct_field='user_content_type', fk_field='user_object_id')

    block_new_version = models.BooleanField(default=True, verbose_name=_('Block new version upload'), help_text=_('Do not allow new version of this document to be uploaded.'))

    # block_metadata
    # block_editing
    # block tag add/remove

    objects = DocumentCheckoutManager()

    def __unicode__(self):
        return unicode(self.document)

    def save(self, *args, **kwargs):
        new_checkout = not self.pk
        if not new_checkout or self.document.is_checked_out():
            raise DocumentAlreadyCheckedOut

        result = super(DocumentCheckout, self).save(*args, **kwargs)
        if new_checkout:
            event_document_check_out.commit(actor=self.user_object, target=self.document)
        return result

    @models.permalink
    def get_absolute_url(self):
        return ('checkout:checkout_info', [self.document.pk])

    class Meta:
        verbose_name = _('Document checkout')
        verbose_name_plural = _('Document checkouts')
