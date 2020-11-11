import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import OperationalError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.celery import app

from mayan.apps.common.compressed_files import Archive
from mayan.apps.common.exceptions import NoMIMETypeMatch
from mayan.apps.lock_manager.exceptions import LockError
from mayan.apps.lock_manager.runtime import locking_backend

from .literals import (
    DEFAULT_SOURCE_LOCK_EXPIRE, DEFAULT_SOURCE_TASK_RETRY_DELAY
)

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_check_interval_source(source_id, test=False):
    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    lock_id = 'task_check_interval_source-%d' % source_id
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        lock = locking_backend.acquire_lock(
            name=lock_id, timeout=DEFAULT_SOURCE_LOCK_EXPIRE
        )
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
    else:
        logger.debug('acquired lock: %s', lock_id)

        try:
            source = Source.objects.get_subclass(pk=source_id)
            if source.enabled or test:
                source.check_source(test=test)
        except Exception as exception:
            logger.error(
                'Error processing source id: %s; %s', source_id, exception
            )
            source.logs.create(
                message=_('Error processing source: %s') % exception
            )
        else:
            source.logs.all().delete()
        finally:
            lock.release()


@app.task()
def task_generate_staging_file_image(staging_folder_pk, encoded_filename, *args, **kwargs):
    StagingFolderSource = apps.get_model(
        app_label='sources', model_name='StagingFolderSource'
    )
    staging_folder = StagingFolderSource.objects.get(pk=staging_folder_pk)
    staging_file = staging_folder.get_file(encoded_filename=encoded_filename)

    return staging_file.generate_image(*args, **kwargs)


@app.task(bind=True, default_retry_delay=DEFAULT_SOURCE_TASK_RETRY_DELAY, ignore_result=True)
def task_source_handle_upload(self, document_type_id, shared_uploaded_file_id, source_id, description=None, expand=False, label=None, language=None, querystring=None, skip_list=None, user_id=None):
    SharedUploadedFile = apps.get_model(
        app_label='common', model_name='SharedUploadedFile'
    )

    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    try:
        document_type = DocumentType.objects.get(pk=document_type_id)
        shared_upload = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )

        if not label:
            label = shared_upload.filename

    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to load data to handle source '
            'upload: %s. Retrying.', exception
        )
        raise self.retry(exc=exception)

    kwargs = {
        'description': description, 'document_type_id': document_type.pk,
        'label': label, 'language': language, 'querystring': querystring,
        'source_id': source_id, 'user_id': user_id
    }

    if not skip_list:
        skip_list = []

    with shared_upload.open() as file_object:
        if expand:
            try:
                compressed_file = Archive.open(file_object=file_object)
                for compressed_file_child in compressed_file.get_members():
                    # TODO: find way to uniquely identify child files
                    # Use filename in the meantime.
                    if force_text(s=compressed_file_child) not in skip_list:
                        kwargs.update(
                            {'label': force_text(s=compressed_file_child)}
                        )

                        try:
                            child_shared_uploaded_file = SharedUploadedFile.objects.create(
                                file=File(compressed_file_child)
                            )
                        except OperationalError as exception:
                            logger.warning(
                                'Operational error while preparing to upload '
                                'child document: %s. Rescheduling.', exception
                            )

                            # TODO: Don't call the task itself again
                            # Update to use celery's retry feature
                            task_source_handle_upload.delay(
                                document_type_id=document_type_id,
                                shared_uploaded_file_id=shared_uploaded_file_id,
                                source_id=source_id, description=description,
                                expand=expand, label=label,
                                language=language,
                                skip_list=skip_list, querystring=querystring,
                                user_id=user_id
                            )
                            return
                        else:
                            skip_list.append(force_text(s=compressed_file_child))
                            task_upload_document.delay(
                                shared_uploaded_file_id=child_shared_uploaded_file.pk,
                                **kwargs
                            )
                        finally:
                            compressed_file_child.close()

                    compressed_file_child.close()
                try:
                    shared_upload.delete()
                except OperationalError as exception:
                    logger.warning(
                        'Operational error during attempt to delete shared '
                        'upload file: %s; %s. Retrying.', shared_upload,
                        exception
                    )
            except NoMIMETypeMatch:
                logger.debug('Exception: NoMIMETypeMatch')
                task_upload_document.delay(
                    shared_uploaded_file_id=shared_upload.pk, **kwargs
                )
        else:
            task_upload_document.delay(
                shared_uploaded_file_id=shared_upload.pk, **kwargs
            )


@app.task(bind=True, default_retry_delay=DEFAULT_SOURCE_TASK_RETRY_DELAY, ignore_result=True)
def task_upload_document(self, source_id, document_type_id, shared_uploaded_file_id, description=None, label=None, language=None, querystring=None, user_id=None):
    SharedUploadedFile = apps.get_model(
        app_label='common', model_name='SharedUploadedFile'
    )

    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    try:
        document_type = DocumentType.objects.get(pk=document_type_id)
        source = Source.objects.get_subclass(pk=source_id)
        shared_upload = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )

        if user_id:
            user = get_user_model().objects.get(pk=user_id)
        else:
            user = None

        with shared_upload.open() as file_object:
            source.upload_document(
                file_object=file_object, document_type=document_type,
                description=description, label=label, language=language,
                querystring=querystring, user=user,
            )

    except OperationalError as exception:
        logger.warning(
            'Operational exception while trying to create new document "%s" '
            'from source id %d; %s. Retying.',
            label or shared_upload.filename, source_id, exception
        )
        raise self.retry(exc=exception)
    else:
        try:
            shared_upload.delete()
        except OperationalError as exception:
            logger.warning(
                'Operational error during attempt to delete shared upload '
                'file: %s; %s. Retrying.', shared_upload, exception
            )
