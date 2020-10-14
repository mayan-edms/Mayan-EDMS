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
    name='documents_periodic', label=_('Documents periodic'), transient=True,
    worker=worker_medium
)
queue_uploads = CeleryQueue(
    name='uploads', label=_('Uploads'), worker=worker_medium
)
queue_documents = CeleryQueue(
    name='documents', label=_('Documents'), worker=worker_medium
)

queue_converter.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_file_page_image_generate',
    label=_('Generate document file page image')
)
queue_converter.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_version_page_image_generate',
    label=_('Generate document version page image')
)

queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_duplicates_clean_empty_lists',
    label=_('Clean empty duplicate lists')
)
queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_trash_can_empty',
    label=_('Empty the trash can')
)
queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_trashed_document_delete',
    label=_('Delete a document')
)
queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_version_page_list_reset',
    label=_('Reset the page list of a document version')
)
queue_documents.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_version_export',
    label=_('Export a document version')
)

queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_type_document_trash_periods_check',
    label=_('Check document type trash periods'),
    name='task_document_type_document_trash_periods_check',
    schedule=timedelta(seconds=CHECK_TRASH_PERIOD_INTERVAL),
)
queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_stubs_delete',
    label=_('Delete document stubs'),
    name='task_document_stubs_delete',
    schedule=timedelta(seconds=DELETE_STALE_STUBS_INTERVAL),
)
queue_documents_periodic.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_type_trashed_document_delete_periods_check',
    label=_('Check document type delete periods'),
    name='task_document_type_trashed_document_delete_periods_check',
    schedule=timedelta(
        seconds=CHECK_DELETE_PERIOD_INTERVAL
    ),
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_duplicates_scan_all',
    label=_('Duplicated document scan')
)

queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_file_page_count_update',
    label=_('Update document page count')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_document_file_upload',
    label=_('Upload new document file')
)
queue_uploads.add_task_type(
    dotted_path='mayan.apps.documents.tasks.task_duplicates_scan_for',
    label=_('Scan document duplicates')
)
