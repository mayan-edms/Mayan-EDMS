import logging

from django.apps import apps
from django.db import OperationalError

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .settings import setting_task_retry

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, default_retry_delay=setting_task_retry.value, max_retries=None,
    ignore_result=True
)
def task_delete_empty(self):
    IndexInstanceNode = apps.get_model(
        app_label='document_indexing', model_name='IndexInstanceNode'
    )

    try:
        IndexInstanceNode.objects.delete_empty()
    except LockError as exception:
        raise self.retry(exc=exception)


@app.task(
    bind=True, default_retry_delay=setting_task_retry.value, max_retries=None,
    ignore_result=True
)
def task_index_document(self, document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )

    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        # Document was deleted before we could execute, abort about
        # updating
        pass
    else:
        try:
            IndexTemplate.objects.index_document(document=document)
        except OperationalError as exception:
            logger.warning(
                'Operational error while trying to index document: '
                '%s; %s', document, exception
            )
            raise self.retry(exc=exception)
        except LockError as exception:
            logger.warning(
                'Unable to acquire lock for document %s; %s ',
                document, exception
            )
            raise self.retry(exc=exception)


@app.task(
    bind=True, default_retry_delay=setting_task_retry.value,
    ignore_result=True
)
def task_rebuild_index(self, index_id):
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )

    try:
        index = IndexTemplate.objects.get(pk=index_id)
        index.rebuild()
    except LockError as exception:
        # This index is being rebuilt by another task, retry later
        raise self.retry(exc=exception)


@app.task(
    bind=True, default_retry_delay=setting_task_retry.value, max_retries=None,
    ignore_result=True
)
def task_remove_document(self, document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    IndexInstanceNode = apps.get_model(
        app_label='document_indexing', model_name='IndexInstanceNode'
    )

    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        # Document was deleted before we could execute
        # Since it was automatically removed from the document M2M
        # we just now delete the empty instance nodes
        try:
            IndexInstanceNode.objects.delete_empty()
        except LockError as exception:
            raise self.retry(exc=exception)
    else:
        try:
            IndexInstanceNode.objects.remove_document(document=document)
        except LockError as exception:
            raise self.retry(exc=exception)
