from datetime import timedelta, datetime
import platform
from time import sleep
from random import random

from django.db.models import Q
from django.core.cache import get_cache

from job_processor.api import process_job

from ocr.api import do_document_ocr
from ocr.literals import QUEUEDOCUMENT_STATE_PENDING, \
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_ACTIVE, \
    QUEUEDOCUMENT_STATE_ERROR
from ocr.models import QueueDocument, DocumentQueue
from ocr.conf.settings import NODE_CONCURRENT_EXECUTION
from ocr.conf.settings import REPLICATION_DELAY
from ocr.conf.settings import CACHE_URI
from ocr.conf.settings import QUEUE_PROCESSING_INTERVAL

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes
# TODO: Tie LOCK_EXPIRATION with hard task timeout

if CACHE_URI:
    try:
        cache_backend = get_cache(CACHE_URI)
    except ImportError:
        # TODO: display or log error
        cache_backend = None
else:
    cache_backend = None


def random_delay():
    sleep(random() * (QUEUE_PROCESSING_INTERVAL - 1))
    return True


if cache_backend:
    acquire_lock = lambda lock_id: cache_backend.add(lock_id, u'true', LOCK_EXPIRE)
    release_lock = lambda lock_id: cache_backend.delete(lock_id)
else:
    acquire_lock = lambda lock_id: True
    release_lock = lambda lock_id: True


def task_process_queue_document(queue_document_id):
    lock_id = u'%s-lock-%d' % (u'task_process_queue_document', queue_document_id)
    if acquire_lock(lock_id):
        queue_document = QueueDocument.objects.get(pk=queue_document_id)
        queue_document.state = QUEUEDOCUMENT_STATE_PROCESSING
        queue_document.node_name = platform.node()
        #queue_document.result = task_process_queue_document.request.id
        queue_document.save()
        try:
            do_document_ocr(queue_document)
            queue_document.delete()
        except Exception, e:
            queue_document.state = QUEUEDOCUMENT_STATE_ERROR
            queue_document.result = e
            queue_document.save()
        release_lock(lock_id)


def reset_orphans():
    pass
    '''
    i = inspect().active()
    active_tasks = []
    orphans = []

    if i:
        for host, instances in i.items():
            for instance in instances:
                active_tasks.append(instance['id'])

    for document_queue in DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE):
        orphans = document_queue.queuedocument_set.\
            filter(state=QUEUEDOCUMENT_STATE_PROCESSING).\
            exclude(result__in=active_tasks)

    for orphan in orphans:
        orphan.result = _(u'Orphaned')
        orphan.state = QUEUEDOCUMENT_STATE_PENDING
        orphan.delay = False
        orphan.node_name = None
        orphan.save()
    '''
    

def task_process_document_queues():
    if not cache_backend:
        random_delay()
    # reset_orphans()
    # Causes problems with big clusters increased latency
    # Disabled until better solution
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
                    #task_process_queue_document.delay(oldest_queued_document.pk)
                    #task_process_queue_document(oldest_queued_document.pk)
                    process_job(task_process_queue_document, oldest_queued_document.pk)
            except Exception, e:
                print 'DocumentQueueWatcher exception: %s' % e
