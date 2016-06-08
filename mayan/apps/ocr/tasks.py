from __future__ import unicode_literals

import logging
import sys
import traceback

from django.apps import apps
from django.conf import settings
from django.db import OperationalError

from documents.models import DocumentVersion
from lock_manager import LockError
from mayan.celery import app

from .classes import TextExtractor
from .literals import DO_OCR_RETRY_DELAY, LOCK_EXPIRE
from .models import DocumentVersionOCRError
from .signals import post_document_version_ocr

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=DO_OCR_RETRY_DELAY, ignore_result=True)
def task_do_ocr(self, document_version_pk):
    Lock = apps.get_model(
        app_label='lock_manager', model_name='Lock'
    )

    lock_id = 'task_do_ocr_doc_version-%d' % document_version_pk
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        # Acquire lock to avoid doing OCR on the same document version more than
        # once concurrently
        lock = Lock.objects.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s', lock_id)
        document_version = None
        try:
            document_version = DocumentVersion.on_organization.get(
                pk=document_version_pk
            )
            logger.info(
                'Starting document OCR for document version: %s',
                document_version
            )
            TextExtractor.process_document_version(document_version)
        except OperationalError as exception:
            logger.warning(
                'OCR error for document version: %d; %s. Retrying.',
                document_version_pk, exception
            )
            raise self.retry(exc=exception)
        except Exception as exception:
            logger.error(
                'OCR error for document version: %d; %s', document_version_pk,
                exception
            )
            if document_version:
                entry, created = DocumentVersionOCRError.on_organization.get_or_create(
                    document_version=document_version
                )

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
            logger.info(
                'OCR complete for document version: %s', document_version
            )
            try:
                entry = DocumentVersionOCRError.on_organization.get(
                    document_version=document_version
                )
            except DocumentVersionOCRError.DoesNotExist:
                pass
            else:
                entry.delete()

            post_document_version_ocr.send(
                sender=self, instance=document_version
            )
        finally:
            lock.release()
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
