from __future__ import unicode_literals

import logging

from django.db import OperationalError

from mayan.celery import app
from documents.models import Document
from lock_manager import Lock, LockError

from .literals import RETRY_DELAY
from .models import IndexInstanceNode

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=RETRY_DELAY, max_retries=None, ignore_result=True)
def task_delete_empty_index_nodes(self):
    try:
        rebuild_lock = Lock.acquire_lock(
            'document_indexing_task_do_rebuild_all_indexes'
        )
    except LockError as exception:
        # A rebuild is happening, retry later
        raise self.retry(exc=exception)
    else:
        try:
            IndexInstanceNode.objects.delete_empty_index_nodes()
        finally:
            rebuild_lock.release()


@app.task(bind=True, default_retry_delay=RETRY_DELAY, max_retries=None, ignore_result=True)
def task_index_document(self, document_id):
    try:
        rebuild_lock = Lock.acquire_lock(
            'document_indexing_task_do_rebuild_all_indexes'
        )
    except LockError as exception:
        # A rebuild is happening, retry later
        raise self.retry(exc=exception)
    else:
        try:
            lock = Lock.acquire_lock(
                'document_indexing_task_update_index_document_%d' % document_id
            )
        except LockError as exception:
            # This document is being reindexed by another task, retry later
            raise self.retry(exc=exception)
        else:
            try:
                document = Document.objects.get(pk=document_id)
            except Document.DoesNotExist:
                # Document was deleted before we could execute, abort about
                # updating
                pass
            else:
                try:
                    IndexInstanceNode.objects.index_document(document)
                except OperationalError as exception:
                    logger.warning(
                        'Operational error while trying to index document: '
                        '%s; %s', document, exception
                    )
                    lock.release()
                    raise self.retry(exc=exception)
                else:
                    lock.release()
            finally:
                lock.release()
        finally:
            rebuild_lock.release()


@app.task(bind=True, default_retry_delay=RETRY_DELAY, ignore_result=True)
def task_do_rebuild_all_indexes(self):
    if Lock.check_existing(name__startswith='document_indexing_task_update_index_document'):
        # A document index update is happening, wait
        raise self.retry()

    try:
        lock = Lock.acquire_lock(
            'document_indexing_task_do_rebuild_all_indexes'
        )
    except LockError as exception:
        # Another rebuild is happening, retry later
        raise self.retry(exc=exception)
    else:
        try:
            IndexInstanceNode.objects.rebuild_all_indexes()
        finally:
            lock.release()
