import logging

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import OperationalError

from mayan.celery import app

from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError

from .literals import DEFAULT_SOURCES_LOCK_EXPIRE

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_source_process_document(source_id, dry_run=False):
    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    lock_id = 'task_source_process_document-%d' % source_id
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        lock = LockingBackend.get_backend().acquire_lock(
            name=lock_id, timeout=DEFAULT_SOURCES_LOCK_EXPIRE
        )
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
    else:
        logger.debug('acquired lock: %s', lock_id)

        try:
            source = Source.objects.get(pk=source_id)
            if source.enabled or dry_run:
                source.get_backend_instance().process_documents(dry_run=dry_run)
        except Exception as exception:
            logger.error(
                'Error processing source id: %s; %s', source_id, exception,
                exc_info=True
            )
            if settings.DEBUG:
                raise
            else:
                source.error_log.create(
                    text='{}; {}'.format(
                        exception.__class__.__name__, exception
                    )
                )
        else:
            source.error_log.all().delete()
        finally:
            lock.release()


@app.task(bind=True, ignore_result=True, retry_backoff=True)
def task_process_document_upload(
    self, document_type_id, shared_uploaded_file_id, source_id,
    callback_kwargs=None, description=None, expand=False, label=None,
    language=None, user_id=None
):
    try:
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        SharedUploadedFile = apps.get_model(
            app_label='storage', model_name='SharedUploadedFile'
        )
        Source = apps.get_model(
            app_label='sources', model_name='Source'
        )

        document_type = DocumentType.objects.get(pk=document_type_id)
        shared_uploaded_file = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )
        source = Source.objects.get(pk=source_id)

        if not label:
            label = shared_uploaded_file.filename

        if user_id:
            user = get_user_model().objects.get(pk=user_id)
        else:
            user = None
    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to load data to handle source '
            'upload: %s. Retrying.', exception
        )
        raise self.retry(exc=exception)
    else:
        with shared_uploaded_file.open() as file_object:
            source.handle_file_object_upload(
                callback_kwargs=callback_kwargs, document_type=document_type,
                description=description, expand=expand,
                file_object=file_object, label=label, language=language,
                user=user
            )

        shared_uploaded_file.delete()
