from datetime import timedelta, datetime
import platform
import time
import random

from django.db.models import Q

from celery.task import PeriodicTask
from celery.decorators import task

from ocr.api import do_document_ocr
from ocr.literals import QUEUEDOCUMENT_STATE_PENDING, \
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_ACTIVE, \
    QUEUEDOCUMENT_STATE_ERROR
from ocr.models import QueueDocument, DocumentQueue
from ocr.conf.settings import NODE_CONCURRENT_EXECUTION
from ocr.conf.settings import REPLICATION_DELAY


@task
def task_process_queue_document(queue_document_id):
    queue_document = QueueDocument.objects.get(id=queue_document_id)
    if queue_document.state == QUEUEDOCUMENT_STATE_PROCESSING:
        #Recheck to avoid race condition
        return
    queue_document.state = QUEUEDOCUMENT_STATE_PROCESSING
    queue_document.node_name = platform.node()
    queue_document.save()
    try:
        do_document_ocr(queue_document.document)
        queue_document.delete()
    except Exception, e:
        queue_document.state = QUEUEDOCUMENT_STATE_ERROR
        queue_document.result = e
        queue_document.save()


class DocumentQueueWatcher(PeriodicTask):
    run_every = timedelta(seconds=5)

    def run(self, **kwargs):
        #Introduce random 0 < t < 1 second delay to further reduce the
        #chance of a race condition
        time.sleep(random.random())
        logger = self.get_logger(**kwargs)
        logger.info('Running queue watcher.')
        logger.debug('Active queues: %s' % DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE))
        q_pending = Q(state=QUEUEDOCUMENT_STATE_PENDING)
        q_delayed = Q(delay=True)
        q_delay_interval = Q(datetime_submitted__lt=datetime.now() - timedelta(seconds=REPLICATION_DELAY))
        for document_queue in DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE):
            logger.debug('Analysing queue: %s' % document_queue)
            if QueueDocument.objects.filter(
                state=QUEUEDOCUMENT_STATE_PROCESSING).filter(
                node_name=platform.node()).count() < NODE_CONCURRENT_EXECUTION:
                try:
                    oldest_queued_document_qs = document_queue.queuedocument_set.filter(
                        (q_pending & ~q_delayed) | (q_pending & q_delayed & q_delay_interval))

                    if oldest_queued_document_qs:
                        oldest_queued_document = oldest_queued_document_qs.order_by('datetime_submitted')[0]
                        task_process_queue_document.delay(oldest_queued_document.id)
                except Exception, e:
                    print 'DocumentQueueWatcher exception: %s' % e
        return True
