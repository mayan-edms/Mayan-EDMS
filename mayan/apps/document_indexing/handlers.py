from __future__ import unicode_literals

from .tasks import task_delete_empty_index_nodes, task_index_document


def document_created_index_update(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].pk)
    )


def document_index_delete(sender, **kwargs):
    task_delete_empty_index_nodes.apply_async()


def document_metadata_index_update(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].document.pk)
    )


def document_metadata_index_post_delete(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].document.pk)
    )
