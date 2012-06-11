from __future__ import absolute_import

from django.db import models

from documents.models import Document

from .exceptions import DocumentNotCheckedOut


class DocumentCheckoutManager(models.Manager):
    def checked_out(self):
        return Document.objects.filter(pk__in=self.model.objects.all().values_list('pk', flat=True))

    def is_document_checked_out(self, document):
        if self.model.objects.filter(document=document):
            return True
        else:
            return False
            
    def check_in_document(self, document):
        try:
            document_checkout = self.model.objects.get(document=document)
        except self.model.DoesNotExist:
            raise DocumentNotCheckedOut
        else:
            document_checkout.delete()
