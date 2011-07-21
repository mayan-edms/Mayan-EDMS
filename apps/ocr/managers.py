from django.db import models
from django.contrib.contenttypes.models import ContentType

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


class QueueTransformationManager(models.Manager):
    def get_for_object(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return self.model.objects.filter(content_type=ct).filter(object_id=obj.pk)

    def get_for_object_as_list(self, obj):
        warnings = []
        transformations = []
        for transformation in self.get_for_object(obj).values('transformation', 'arguments'):
            try:
                transformations.append(
                    {
                        'transformation': transformation['transformation'],
                        'arguments': eval(transformation['arguments'], {})
                    }
                )
            except Exception, e:
                warnings.append(e)

        return transformations, warnings
