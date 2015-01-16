from __future__ import unicode_literals

import logging
import sys
import traceback

from django.conf import settings

from documents.models import DocumentVersion
from lock_manager import Lock, LockError
from mayan.celery import app

from .api import do_document_ocr
from .literals import LOCK_EXPIRE
from .models import DocumentVersionOCRError

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_do_ocr(document_version_pk):
    lock_id = 'task_do_ocr_doc_version-%d' % document_version_pk
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        # Acquire lock to avoid doing OCR on the same document version more than
        # once concurrently
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s', lock_id)
        document_version = None
        try:
            logger.info('Starting document OCR for document version: %d', document_version_pk)
            document_version = DocumentVersion.objects.get(pk=document_version_pk)
            do_document_ocr(document_version)
        except Exception as exception:
            logger.error('OCR error for document version: %d; %s', document_version_pk, exception)
            if document_version:
                entry, created = DocumentVersionOCRError.objects.get_or_create(document_version=document_version)

                if settings.DEBUG:
                    result = []
                    type, value, tb = sys.exc_info()
                    result.append('%s: %s' % (type.__name__, value))
                    result.extend(traceback.format_tb(tb))
                    entry.result = '\n'.join(result)
                else:
                    entry.result = exception

                entry.save()
        else:
            logger.info('OCR for document: %d ended', document_version_pk)
            try:
                entry = DocumentVersionOCRError.objects.get(document_version=document_version)
            except DocumentVersionOCRError.DoesNotExist:
                pass
            else:
                entry.delete()
        finally:
            lock.release()
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
        pass
