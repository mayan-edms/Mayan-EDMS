from __future__ import absolute_import, unicode_literals

from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_fast, worker_medium

from .literals import (
    CHECK_DELETE_PERIOD_INTERVAL, CHECK_TRASH_PERIOD_INTERVAL,
    DELETE_STALE_STUBS_INTERVAL
)

queue_converter = CeleryQueue(
    name='converter', label=_('Converter'), transient=True, worker=worker_fast
)
queue_documents_periodic = CeleryQueue(
    name='documents_periodic', label=_('Documents periodic'), transient=True, worker=worker_medium
)
queue_uploads = CeleryQueue(
    name='uploads', label=_('Uploads'), worker=worker_medium
)
queue_documents = CeleryQueue(
    name='documents', label=_('Documents'), worker=worker_medium
)

queue_converter.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_generate_document_page_image',
    label=_('Generate document page image')
)
queue_converter.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_generate_document_version_page_image',
    label=_('Generate document version page image')
)

queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_delete_document',
    label=_('Delete a document')
)
queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_clean_empty_duplicate_lists',
    label=_('Clean empty duplicate lists')
)

queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_check_delete_periods',
    label=_('Check document type delete periods'),
    name='task_check_delete_periods',
    schedule=timedelta(
        seconds=CHECK_DELETE_PERIOD_INTERVAL
    ),
)
queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_check_trash_periods',
    label=_('Check document type trash periods'),
    name='task_check_trash_periods',
    schedule=timedelta(seconds=CHECK_TRASH_PERIOD_INTERVAL),
)
queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_delete_stubs',
    label=_('Delete document stubs'),
    name='task_delete_stubs',
    schedule=timedelta(seconds=DELETE_STALE_STUBS_INTERVAL),
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_scan_duplicates_all',
    label=_('Duplicated document scan')
)

queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_pages_reset',
    label=_('Reset document pages')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_update_page_count',
    label=_('Update document page count')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_upload_new_version',
    label=_('Upload new document version')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_scan_duplicates_for',
    label=_('Scan document duplicates')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_upload_new_document',
    label=_('Upload new document')
)
