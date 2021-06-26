import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import OperationalError

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .literals import (
    UPDATE_PAGE_COUNT_RETRY_DELAY, UPLOAD_NEW_VERSION_RETRY_DELAY
)
from .settings import (
    setting_task_document_file_page_image_generate_retry_delay,
    setting_task_document_version_page_image_generate_retry_delay
)

logger = logging.getLogger(name=__name__)


# Document

@app.task(ignore_result=True)
def task_document_stubs_delete():
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )

    logger.info(msg='Executing')
    Document.objects.delete_stubs()
    logger.info(msg='Finished')


# Document file

@app.task(
    bind=True, default_retry_delay=UPDATE_PAGE_COUNT_RETRY_DELAY,
    ignore_result=True
)
def task_document_file_page_count_update(self, document_file_id):
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    document_file = DocumentFile.objects.get(pk=document_file_id)
    try:
        document_file.page_count_update()
    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to update page count for '
            'document file: %s; %s. Retrying.', document_file,
            exception
        )
        raise self.retry(exc=exception)


@app.task(
    bind=True,
    default_retry_delay=setting_task_document_file_page_image_generate_retry_delay.value
)
def task_document_file_page_image_generate(
    self, document_file_page_id, user_id=None, **kwargs
):
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )
    User = get_user_model()

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    document_file_page = DocumentFilePage.objects.get(pk=document_file_page_id)
    try:
        return document_file_page.generate_image(user=user, **kwargs)
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate document page image for '
            'document id: %d, document file id: %d, document file '
            'page id: %d. Retrying.',
            document_file_page.document_file.document_id,
            document_file_page.document_file_id,
            document_file_page.pk,
        )
        raise self.retry(exc=exception)


@app.task(
    bind=True, default_retry_delay=UPLOAD_NEW_VERSION_RETRY_DELAY,
    ignore_result=True
)
def task_document_file_upload(
    self, document_id, shared_uploaded_file_id, user_id=None, action=None,
    comment=None, filename=None
):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )

    SharedUploadedFile = apps.get_model(
        app_label='storage', model_name='SharedUploadedFile'
    )

    try:
        document = Document.objects.get(pk=document_id)
        shared_file = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )
        if user_id:
            user = get_user_model().objects.get(pk=user_id)
        else:
            user = None

    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to retrieve shared data for '
            'new document file for document ID: %s; %s. Retrying.', document_id,
            exception
        )
        raise self.retry(exc=exception)

    with shared_file.open() as file_object:
        try:
            document.file_new(
                action=action, comment=comment, file_object=file_object,
                filename=filename or shared_file.filename, _user=user
            )
        except Warning as warning:
            # New document file are blocked
            logger.info(
                'Warning during attempt to create new document file for '
                'document: %s; %s', document, warning
            )
            shared_file.delete()
        except OperationalError as exception:
            logger.warning(
                'Operational error during attempt to create new document '
                'file for document: %s; %s. Retrying.', document, exception
            )
            raise self.retry(exc=exception)
        except Exception as exception:
            # This except and else block emulate a finally:
            logger.error(
                'Unexpected error during attempt to create new document '
                'file for document: %s; %s', document, exception,
                exc_info=True
            )
            try:
                shared_file.delete()
            except OperationalError as exception:
                logger.warning(
                    'Operational error during attempt to delete shared '
                    'file: %s; %s.', shared_file, exception
                )
        else:
            try:
                shared_file.delete()
            except OperationalError as exception:
                logger.warning(
                    'Operational error during attempt to delete shared '
                    'file: %s; %s.', shared_file, exception
                )


# Document type

@app.task(ignore_result=True)
def task_document_type_trashed_document_delete_periods_check():
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    DocumentType.objects.check_delete_periods()


@app.task(ignore_result=True)
def task_document_type_document_trash_periods_check():
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    DocumentType.objects.check_trash_periods()


# Document version

@app.task(ignore_result=True)
def task_document_version_page_list_reset(document_version_id):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(
        pk=document_version_id
    )
    document_version.pages_reset()


@app.task(ignore_result=True)
def task_document_version_export(
    document_version_id, organization_installation_url=None, user_id=None
):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    User = get_user_model()

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    document_version = DocumentVersion.objects.get(
        pk=document_version_id
    )

    document_version.export_to_download_file(
        organization_installation_url=organization_installation_url, user=user
    )


# Document version page

@app.task(
    bind=True,
    default_retry_delay=setting_task_document_version_page_image_generate_retry_delay.value
)
def task_document_version_page_image_generate(
    self, document_version_page_id, user_id=None, **kwargs
):
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )
    User = get_user_model()

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    document_version_page = DocumentVersionPage.objects.get(
        pk=document_version_page_id
    )
    try:
        return document_version_page.generate_image(user=user, **kwargs)
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate document page image for '
            'document id: %d, document version id: %d, document version '
            'page id: %d. Retrying.',
            document_version_page.document_version.document_id,
            document_version_page.document_version_id,
            document_version_page.pk,
        )
        raise self.retry(exc=exception)


# Trash can

@app.task(ignore_result=True)
def task_trash_can_empty():
    TrashedDocument = apps.get_model(
        app_label='documents', model_name='TrashedDocument'
    )

    for trashed_document in TrashedDocument.objects.all():
        task_trashed_document_delete.apply_async(
            kwargs={'trashed_document_id': trashed_document.pk}
        )


# Trashed document

@app.task(ignore_result=True)
def task_trashed_document_delete(trashed_document_id):
    TrashedDocument = apps.get_model(
        app_label='documents', model_name='TrashedDocument'
    )

    logger.debug(msg='Executing')
    trashed_document = TrashedDocument.objects.get(pk=trashed_document_id)
    trashed_document.delete()
    logger.debug(msg='Finished')
