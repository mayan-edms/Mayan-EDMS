from datetime import date, timedelta
from celery.task import Task, PeriodicTask
from celery.decorators import task

from documents import Document

from ocr.api import do_document_ocr
from literals import QUEUEDOCUMENT_STATE_PENDING, \
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_ACTIVE, \
    QUEUEDOCUMENT_STATE_ERROR
from models import QueueDocument, DocumentQueue
from ocr.conf.settings import MAX_CONCURRENT_EXECUTION
from ocr.conf.settings import REPLICATION_DELAY

    
@task
def task_process_queue_document(queue_document_id):
    queue_document = QueueDocument.objects.get(id=queue_document_id)
    queue_document.state = QUEUEDOCUMENT_STATE_PROCESSING
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
        logger = self.get_logger(**kwargs)
        logger.info('Running queue watcher.')
        logger.debug('Active queues: %s' % DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE))
        for document_queue in DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE):
            logger.debug('Analysing queue: %s' % document_queue)
            current_running_queues = QueueDocument.objects.filter(state=QUEUEDOCUMENT_STATE_PROCESSING).count()
            if current_running_queues < MAX_CONCURRENT_EXECUTION:
                try:
                    oldest_queued_document = document_queue.queuedocument_set.filter(
                            state=QUEUEDOCUMENT_STATE_PENDING).filter(datetime_submitted__lt=datetime.datetime.now()-datetime.timedelta(seconds=REPLICATION_DELAY)).order_by('datetime_submitted')[0]

                    task_process_queue_document(oldest_queued_document.id).delay()
                except:
                    #No Documents in queue
                    pass
        return True
