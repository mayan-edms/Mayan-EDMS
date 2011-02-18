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

@task()    
def do_document_ocr_task(document_id):
    document = Document.objects.get(id=document_id)
    do_document_ocr(document)
    
    
@task()
def do_queue_document(queue_document_id):
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
        for document_queue in DocumentQueue.objects.filter(state=DOCUMENTQUEUE_STATE_ACTIVE):
            current_running_queues = QueueDocument.objects.filter(state=QUEUEDOCUMENT_STATE_PROCESSING).count()
            if current_running_queues < MAX_CONCURRENT_EXECUTION:
                try:
                    oldest_queued_document = document_queue.queuedocument_set.filter(
                            state=QUEUEDOCUMENT_STATE_PENDING).order_by('datetime_submitted')[0]

                    do_queue_document(oldest_queued_document.id).delay()
                except:
                    #No Documents in queue
                    pass
        return True
