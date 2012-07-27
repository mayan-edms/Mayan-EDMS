from __future__ import absolute_import

import datetime
import logging

from django.db import models
from django.core.exceptions import PermissionDenied

from documents.models import Document
from permissions.models import Permission
from acls.models import AccessEntry

from .exceptions import DocumentNotCheckedOut
from .literals import STATE_CHECKED_OUT, STATE_CHECKED_IN
from .events import (history_document_checked_in, history_document_auto_checked_in,
    history_document_forceful_check_in)
from .permissions import PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE

logger = logging.getLogger(__name__)


class DocumentCheckoutManager(models.Manager):
    def checked_out_documents(self):
        return Document.objects.filter(pk__in=self.model.objects.all().values_list('document__pk', flat=True))

    def expired_check_outs(self):
        expired_list = Document.objects.filter(pk__in=self.model.objects.filter(expiration_datetime__lte=datetime.datetime.now()).values_list('document__pk', flat=True))
        logger.debug('expired_list: %s' % expired_list)
        return expired_list

    def check_in_expired_check_outs(self):
        for document in self.expired_check_outs():
            document.check_in()

    def is_document_checked_out(self, document):
        if self.model.objects.filter(document=document):
            return True
        else:
            return False

    def check_in_document(self, document, user=None):
        try:
            document_checkout = self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut
        else:
            if user:
                if self.document_checkout_info(document).user_object != user:
                    history_document_forceful_check_in.commit(source_object=document, data={'user': user, 'document': document})
                else:
                    history_document_checked_in.commit(source_object=document, data={'user': user, 'document': document})
            else:
                history_document_auto_checked_in.commit(source_object=document, data={'document': document})

            document_checkout.delete()

    def document_checkout_info(self, document):
        try:
            return self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut

    def document_checkout_state(self, document):
        if self.is_document_checked_out(document):
            return STATE_CHECKED_OUT
        else:
            return STATE_CHECKED_IN

    def is_document_new_versions_allowed(self, document, user=None):
        try:
            checkout_info = self.document_checkout_info(document)
        except DocumentNotCheckedOut:
            return True
        else:
            if not user:
                return not checkout_info.block_new_version
            else:
                if user.is_staff or user.is_superuser:
                    # Allow anything to superusers and staff
                    return True

                if user == checkout_info.user_object:
                    # Allow anything to the user who checked out this document
                    True
                else:
                    # If not original user check to see if user has global or this document's PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE permission
                    try:
                        Permission.objects.check_permissions(user, [PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE])
                    except PermissionDenied:
                        try:
                            AccessEntry.objects.check_accesses([PERMISSION_DOCUMENT_RESTRICTIONS_OVERRIDE], user, document)
                        except PermissionDenied:
                            # Last resort check if original user enabled restriction
                            return not checkout_info.block_new_version
                        else:
                            return True
                    else:
                        return True
