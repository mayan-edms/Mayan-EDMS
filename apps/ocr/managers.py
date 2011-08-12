from django.db import models

from ocr.exceptions import AlreadyQueued


class DocumentQueueManager(models.Manager):
    """
    Module manager class to handle adding documents to an OCR document
    queue
    """
    def queue_document(self, document, queue_name='default'):
        document_queue = self.model.objects.get(name=queue_name)
        if document_queue.queuedocument_set.filter(document=document):
            raise AlreadyQueued

        document_queue.queuedocument_set.create(document=document, delay=True)

        return document_queue
