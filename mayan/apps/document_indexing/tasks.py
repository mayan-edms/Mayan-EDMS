import logging

from django.apps import apps
from django.db import OperationalError

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

logger = logging.getLogger(name=__name__)


# Index instance

@app.task(
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True,
    retry_backoff_max=60
)
def task_index_instance_document_add(self, document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    IndexInstance = apps.get_model(
        app_label='document_indexing', model_name='IndexInstance'
    )

    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        """
        Document was deleted before we could execute, abort about updating.
        """
    else:
        try:
            IndexInstance.objects.document_add(document=document)
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
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True
)
def task_index_instance_document_remove(self, document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    IndexInstance = apps.get_model(
        app_label='document_indexing', model_name='IndexInstance'
    )

    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        # Document was deleted before we could execute
        # Since it was automatically removed from the document M2M
        # we just now delete the empty instance nodes
        try:
            IndexInstance.objects.delete_empty_nodes()
        except LockError as exception:
            raise self.retry(exc=exception)
    else:
        try:
            IndexInstance.objects.document_remove(document=document)
        except LockError as exception:
            raise self.retry(exc=exception)


@app.task(
    bind=True, ignore_result=True, max_retries=None, retry_backoff=True
)
def task_index_instance_node_delete_empty(self):
    IndexInstance = apps.get_model(
        app_label='document_indexing', model_name='IndexInstance'
    )

    try:
        IndexInstance.objects.delete_empty_nodes()
    except LockError as exception:
        raise self.retry(exc=exception)


# Index template

@app.task(bind=True, ignore_result=True, retry_backoff=True)
def task_index_template_rebuild(self, index_id):
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )

    try:
        index = IndexTemplate.objects.get(pk=index_id)
        index.rebuild()
    except LockError as exception:
        # This index is being rebuilt by another task, retry later
        raise self.retry(exc=exception)
