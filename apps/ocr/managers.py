from __future__ import absolute_import

from django.db import models

#from .exceptions import AlreadyQueued


class OCRProcessingManager(models.Manager):
    """
    Module manager class to handle adding documents to an OCR queue
    """
    def queue_document(self, document):
        pass
        #document_queue = self.model.objects.get(name=queue_name)
        #if document_queue.queuedocument_set.filter(document_version=document.latest_version):
        #    raise AlreadyQueued

        #document_queue.queuedocument_set.create(document_version=document.latest_version, delay=True)

        #return document_queue
