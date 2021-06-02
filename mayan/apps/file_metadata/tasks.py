import logging

from django.apps import apps

from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .literals import LOCK_EXPIRE

from .classes import FileMetadataDriver

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_process_document_file(document_file_id):
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    document_file = DocumentFile.objects.get(pk=document_file_id)

    lock_id = 'task_process_document_file-%d' % document_file_id
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        # Acquire lock to avoid processing the same document file more
        # than once concurrently
        lock = LockingBackend.get_backend().acquire_lock(name=lock_id, timeout=LOCK_EXPIRE)
        logger.debug('acquired lock: %s', lock_id)
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
    else:
        try:
            FileMetadataDriver.process_document_file(
                document_file=document_file
            )
        finally:
            lock.release()
