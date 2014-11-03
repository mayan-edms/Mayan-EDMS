from __future__ import absolute_import

import logging
import platform
import sys
import traceback

from django.conf import settings

from documents.models import Document
from lock_manager import Lock, LockError
from mayan.celery import app

from .api import do_document_ocr
from .models import DocumentQueue, QueueDocument

logger = logging.getLogger(__name__)
LOCK_EXPIRE = 60 * 10  # Adjust to worst case scenario


@app.task(ignore_result=True)
def task_do_ocr(document_pk):
    lock_id = u'task_do_ocr_doc-%d' % document_pk
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        # Acquire lock to avoid doing OCR on the same document more than once
        # concurrently
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s', lock_id)
        document = None
        try:
            logger.info('Starting document OCR for document: %d', document_pk)
            document = Document.objects.get(pk=document_pk)
            do_document_ocr(document)
        except Exception as exception:
            logger.error('OCR error for document: %d; %s', document_pk, exception)
            document_queue = DocumentQueue.objects.get(name='default')
            if document:
                queue_document, created = document_queue.documents.get_or_create(document=document)
                queue_document.node_name = platform.node()

                if settings.DEBUG:
                    result = []
                    type, value, tb = sys.exc_info()
                    result.append('%s: %s' % (type.__name__, value))
                    result.extend(traceback.format_tb(tb))
                    queue_document.result = '\n'.join(result)
                else:
                    queue_document.result = exception

                queue_document.save()
        else:
            logger.info('OCR for document: %d ended', document_pk)
            document_queue = DocumentQueue.objects.get(name='default')
            try:
                queue_document = document_queue.documents.get(document=document)
            except QueueDocument.DoesNotExist:
                pass
            else:
                queue_document.delete()
        finally:
            lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
        pass
