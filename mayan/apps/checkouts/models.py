from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

from .events import event_document_check_out
from .exceptions import DocumentAlreadyCheckedOut
from .managers import DocumentCheckoutManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class DocumentCheckout(models.Model):
    """
    Model to store the state and information of a document checkout
    """
    document = models.ForeignKey(Document, verbose_name=_('Document'), unique=True)
    checkout_datetime = models.DateTimeField(verbose_name=_('Check out date and time'), auto_now_add=True)
    expiration_datetime = models.DateTimeField(verbose_name=_('Check out expiration date and time'), help_text=_('Amount of time to hold the document checked out in minutes.'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))

    block_new_version = models.BooleanField(default=True, verbose_name=_('Block new version upload'), help_text=_('Do not allow new version of this document to be uploaded.'))

    # block_metadata
    # block_editing
    # block tag add/remove

    objects = DocumentCheckoutManager()

    def __str__(self):
        return unicode(self.document)

    def save(self, *args, **kwargs):
        new_checkout = not self.pk
        if not new_checkout or self.document.is_checked_out():
            raise DocumentAlreadyCheckedOut

        result = super(DocumentCheckout, self).save(*args, **kwargs)
        if new_checkout:
            event_document_check_out.commit(actor=self.user, target=self.document)
        return result

    def get_absolute_url(self):
        return reverse('checkout:checkout_info', args=[self.document.pk])

    class Meta:
        verbose_name = _('Document checkout')
        verbose_name_plural = _('Document checkouts')
