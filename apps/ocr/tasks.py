from __future__ import absolute_import

from datetime import timedelta, datetime
import platform
import logging

from django.db.models import Q

from job_processor.api import process_job
from lock_manager import Lock, LockError

from .api import do_document_ocr
from .literals import (QUEUEDOCUMENT_STATE_PENDING,
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_ACTIVE,
    QUEUEDOCUMENT_STATE_ERROR)
from .models import QueueDocument, DocumentQueue
from .conf.settings import (NODE_CONCURRENT_EXECUTION, REPLICATION_DELAY,
    QUEUE_PROCESSING_INTERVAL)

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes
# TODO: Tie LOCK_EXPIRATION with hard task timeout

logger = logging.getLogger(__name__)


def task_process_queue_document(queue_document_id):
    lock_id = u'task_proc_queue_doc-%d' % queue_document_id
    try:
        logger.debug('trying to acquire lock: %s' % lock_id)
        lock = Lock.acquire_lock(lock_id, LOCK_EXPIRE)
        logger.debug('acquired lock: %s' % lock_id)
        queue_document = QueueDocument.objects.get(pk=queue_document_id)
        queue_document.state = QUEUEDOCUMENT_STATE_PROCESSING
        queue_document.node_name = platform.node()
        queue_document.save()
        try:
            do_document_ocr(queue_document)
            queue_document.delete()
        except Exception, e:
            queue_document.state = QUEUEDOCUMENT_STATE_ERROR
            queue_document.result = e
            queue_document.save()

        lock.release()
    except LockError:
        logger.debug('unable to obtain lock')
        pass


def task_process_document_queues():
    logger.debug('executed')
    # TODO: reset_orphans()
    q_pending = Q(state=QUEUEDOCUMENT_STATE_PENDING)
    q_delayed = Q(delay=True)
    q_delay_interval = Q(datetime_submitted__lt=datetime.now() - timedelta(seconds=REPLICATION_DELAY))
    for document_queue in DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE):
        current_local_processing_count = QueueDocument.objects.filter(
            state=QUEUEDOCUMENT_STATE_PROCESSING).filter(
            node_name=platform.node()).count()
        if current_local_processing_count < NODE_CONCURRENT_EXECUTION:
            try:
                oldest_queued_document_qs = document_queue.queuedocument_set.filter(
                    (q_pending & ~q_delayed) | (q_pending & q_delayed & q_delay_interval))

                if oldest_queued_document_qs:
                    oldest_queued_document = oldest_queued_document_qs.order_by('datetime_submitted')[0]
                    process_job(task_process_queue_document, oldest_queued_document.pk)
            except Exception, e:
                logger.error('unhandled exception: %s' % e)
            finally:
                # Don't process anymore from this queryset, might be stale
                break
        else:
            logger.debug('already processing maximun')
    else:
        logger.debug('nothing to process')
