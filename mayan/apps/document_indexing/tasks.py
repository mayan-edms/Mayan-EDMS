from __future__ import unicode_literals

import logging

from mayan.celery import app
from documents.models import Document
from lock_manager import Lock, LockError

from .api import index_document, delete_empty_index_nodes
from .tools import do_rebuild_all_indexes

logger = logging.getLogger(__name__)
RETRY_DELAY = 20  # TODO: convert this into a config option


@app.task(bind=True, ignore_result=True)
def task_delete_empty_index_nodes(self):
    try:
        rebuild_lock = Lock.acquire_lock('document_indexing_task_do_rebuild_all_indexes')
    except LockError as exception:
        # A rebuild is happening, retry later
        raise self.retry(exc=exception, countdown=RETRY_DELAY)
    else:
        try:
            delete_empty_index_nodes()
        finally:
            rebuild_lock.release()


@app.task(bind=True, ignore_result=True)
def task_index_document(self, document_id):
    try:
        rebuild_lock = Lock.acquire_lock('document_indexing_task_do_rebuild_all_indexes')
    except LockError as exception:
        # A rebuild is happening, retry later
        raise self.retry(exc=exception, countdown=RETRY_DELAY)
    else:
        try:
            lock = Lock.acquire_lock('document_indexing_task_update_index_document_%d' % document_id)
        except LockError as exception:
            # This document is being reindexed by another task, retry later
            raise self.retry(exc=exception, countdown=RETRY_DELAY)
        else:
            try:
                document = Document.objects.get(pk=document_id)
            except Document.DoesNotExist:
                # Document was deleted before we could execute, abort about updating
                pass
            else:
                index_document(document)
            finally:
                lock.release()
        finally:
            rebuild_lock.release()


@app.task(bind=True, ignore_result=True)
def task_do_rebuild_all_indexes(self):
    if Lock.filter(name__startswith='document_indexing_task_update_index_document'):
        # A document index update is happening, wait
        raise self.retry(countdown=RETRY_DELAY)

    try:
        lock = Lock.acquire_lock('document_indexing_task_do_rebuild_all_indexes')
    except LockError as exception:
        # Another rebuild is happening, retry later
        raise self.retry(exc=exception, countdown=RETRY_DELAY)
    else:
        try:
            do_rebuild_all_indexes()
        finally:
            lock.release()
