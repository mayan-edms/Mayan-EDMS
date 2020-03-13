from __future__ import unicode_literals

import logging

from mayan.apps.document_indexing.tasks import task_index_document

logger = logging.getLogger(name=__name__)


def handler_index_document(sender, **kwargs):
    if kwargs['action'] in ('post_add', 'post_remove'):
        for pk in kwargs['pk_set']:
            task_index_document.apply_async(kwargs=dict(document_id=pk))


def handler_tag_pre_delete(sender, **kwargs):
    for document in kwargs['instance'].documents.all():
        # Remove each of the documents from the tag
        # Trigger the m2m_changed signal for each document so they can be
        # reindexed
        kwargs['instance'].documents.remove(document)
