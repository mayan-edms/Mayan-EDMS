from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.db import models
from django.utils.timezone import now

from documents.models import Document

from .events import (
    event_document_auto_check_in, event_document_check_in,
    event_document_forceful_check_in
)
from .exceptions import DocumentNotCheckedOut
from .literals import STATE_CHECKED_OUT, STATE_CHECKED_IN

logger = logging.getLogger(__name__)


class DocumentCheckoutManager(models.Manager):
    def are_document_new_versions_allowed(self, document, user=None):
        try:
            checkout_info = self.document_checkout_info(document)
        except DocumentNotCheckedOut:
            return True
        else:
            return not checkout_info.block_new_version

    def check_in_document(self, document, user=None):
        try:
            document_checkout = self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut
        else:
            if user:
                if self.document_checkout_info(document=document).user != user:
                    event_document_forceful_check_in.commit(
                        actor=user, target=document
                    )
                else:
                    event_document_check_in.commit(actor=user, target=document)
            else:
                event_document_auto_check_in.commit(target=document)

            document_checkout.delete()

    def check_in_expired_check_outs(self):
        for document in self.expired_check_outs():
            document.check_in()

    def checkout_document(self, document, expiration_datetime, user, block_new_version=True):
        return self.create(
            block_new_version=block_new_version, document=document,
            expiration_datetime=expiration_datetime, user=user
        )

    def checked_out_documents(self):
        return Document.objects.filter(
            pk__in=self.model.objects.values('document__id')
        )

    def document_checkout_info(self, document):
        try:
            return self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut

    def document_checkout_state(self, document):
        if self.is_document_checked_out(document=document):
            return STATE_CHECKED_OUT
        else:
            return STATE_CHECKED_IN

    def expired_check_outs(self):
        expired_list = Document.objects.filter(
            pk__in=self.model.objects.filter(
                expiration_datetime__lte=now()
            ).values_list('document__pk', flat=True)
        )
        logger.debug('expired_list: %s', expired_list)
        return expired_list

    def get_by_natural_key(self, document_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        try:
            document = Document.objects.get_by_natural_key(document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document__pk=document.pk)

    def is_document_checked_out(self, document):
        return self.filter(document=document).exists()


class NewVersionBlockManager(models.Manager):
    def block(self, document):
        self.get_or_create(document=document)

    def is_blocked(self, document):
        return self.filter(document=document).exists()

    def get_by_natural_key(self, document_natural_key):
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        try:
            document = Document.objects.get_by_natural_key(document_natural_key)
        except Document.DoesNotExist:
            raise self.model.DoesNotExist

        return self.get(document__pk=document.pk)

    def unblock(self, document):
        self.filter(document=document).delete()
