import logging

from mayan.apps.document_indexing.tasks import task_index_instance_document_add

logger = logging.getLogger(name=__name__)


def handler_index_document(sender, **kwargs):
    if not kwargs.get('created', False):
        for document in kwargs['instance'].documents.all():
            task_index_instance_document_add.apply_async(
                kwargs={'document_id': document.pk}
            )


def handler_cabinet_pre_delete(sender, **kwargs):
    for document in kwargs['instance'].documents.all():
        # Remove each of the related documents.
        # Trigger the remove event for each document so they can be
        # reindexed.
        kwargs['instance'].document_remove(document=document)
