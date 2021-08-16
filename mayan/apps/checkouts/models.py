import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models import Document
from mayan.apps.events.classes import EventManagerMethodAfter
from mayan.apps.events.decorators import method_event

from .events import (
    event_document_auto_checked_in, event_document_checked_in,
    event_document_checked_out, event_document_forcefully_checked_in
)
from .exceptions import DocumentAlreadyCheckedOut
from .managers import (
    DocumentCheckoutBusinessLogicManager, DocumentCheckoutManager
)

logger = logging.getLogger(name=__name__)


class DocumentCheckout(ExtraDataModelMixin, models.Model):
    """
    Model to store the state and information of a document checkout.
    """
    document = models.OneToOneField(
        on_delete=models.CASCADE, to=Document, verbose_name=_('Document')
    )
    checkout_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Check out date and time')
    )
    expiration_datetime = models.DateTimeField(
        help_text=_(
            'Amount of time to hold the document checked out in minutes.'
        ),
        verbose_name=_('Check out expiration date and time')
    )
    user = models.ForeignKey(
        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL,
        verbose_name=_('User')
    )
    block_new_file = models.BooleanField(
        default=True,
        help_text=_(
            'Do not allow new file of this document to be uploaded.'
        ),
        verbose_name=_('Block new file upload')
    )

    objects = DocumentCheckoutManager()
    business_logic = DocumentCheckoutBusinessLogicManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Document checkout')
        verbose_name_plural = _('Document checkouts')

    def __str__(self):
        return force_text(s=self.document)

    def clean(self):
        if self.expiration_datetime < now():
            raise ValidationError(
                _('Check out expiration date and time must be in the future.')
            )

    @method_event(event_manager_class=EventManagerMethodAfter)
    def delete(self, user=None):
        self._event_target = self.document
        self._event_actor = user or getattr(self, '_event_actor', None)

        if self._event_actor:
            if self._event_actor == self.user:
                self._event_type = event_document_checked_in
            else:
                self._event_type = event_document_forcefully_checked_in
        else:
            self._event_type = event_document_auto_checked_in

        return super().delete()

    def get_absolute_url(self):
        return reverse(
            viewname='checkouts:check_out_info', kwargs={
                'document_id': self.document_id
            }
        )

    def natural_key(self):
        return self.document.natural_key()
    natural_key.dependencies = ['documents.Document']

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if not is_new or self.document.is_checked_out():
            raise DocumentAlreadyCheckedOut

        result = super().save(*args, **kwargs)
        if is_new:
            event_document_checked_out.commit(
                actor=self.user, target=self.document
            )

            logger.info(
                'Document "%s" checked out by user "%s"',
                self.document, self.user
            )

        return result


class CheckedOutDocument(Document):
    class Meta:
        proxy = True

    def get_user_display(self):
        check_out_info = self.get_check_out_info()
        return check_out_info.user.get_full_name() or check_out_info.user

    get_user_display.short_description = _('User')

    def get_checkout_datetime(self):
        return self.get_check_out_info().checkout_datetime

    get_checkout_datetime.short_description = _('Checkout time and date')

    def get_checkout_expiration(self):
        return self.get_check_out_info().expiration_datetime

    get_checkout_expiration.short_description = _('Checkout expiration')
