import logging

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import OperationalError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.lock_manager.exceptions import LockError
from mayan.celery import app

from .literals import (
    UPDATE_PAGE_COUNT_RETRY_DELAY, UPLOAD_NEW_VERSION_RETRY_DELAY
)
from .permissions import permission_document_version_export
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
    logger.info(msg='Finshed')


# Document file

@app.task(bind=True, default_retry_delay=UPDATE_PAGE_COUNT_RETRY_DELAY, ignore_result=True)
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


@app.task(bind=True, default_retry_delay=UPLOAD_NEW_VERSION_RETRY_DELAY, ignore_result=True)
def task_document_file_upload(self, document_id, shared_uploaded_file_id, user_id, action=None, comment=None):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )

    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
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
            'new document file for:%s; %s. Retrying.', document, exception
        )
        raise self.retry(exc=exception)

    with shared_file.open() as file_object:
        try:
            document_file = document.new_file(
                action=action, comment=comment, file_object=file_object,
                _user=user
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
                'file for document: %s; %s', document, exception
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
def task_document_version_export(document_version_id):
    DownloadFile = apps.get_model(
        app_label='storage', model_name='DownloadFile'
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(
        pk=document_version_id
    )

    download_file = DownloadFile.objects.create(
        content_object=document_version,
        filename='{}.pdf'.format(document_version),
        label=_('Document version export to PDF'),
        permission=permission_document_version_export.stored_permission
    )

    with download_file.open(mode='wb+') as file_object:
        document_version.export(file_object=file_object)


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


# Duplicates

@app.task(ignore_result=True)
def task_duplicates_clean_empty_lists():
    DuplicatedDocument = apps.get_model(
        app_label='documents', model_name='DuplicatedDocument'
    )
    DuplicatedDocument.objects.clean_empty_duplicate_lists()

@app.task(ignore_result=True)
def task_duplicates_scan_all():
    DuplicatedDocument = apps.get_model(
        app_label='documents', model_name='DuplicatedDocument'
    )

    DuplicatedDocument.objects.scan()


@app.task(ignore_result=True)
def task_duplicates_scan_for(document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    DuplicatedDocument = apps.get_model(
        app_label='documents', model_name='DuplicatedDocument'
    )

    document = Document.objects.get(pk=document_id)

    DuplicatedDocument.objects.scan_for(document=document)


# Trash can

@app.task(ignore_result=True)
def task_trash_can_empty():
    DeletedDocument = apps.get_model(
        app_label='documents', model_name='DeletedDocument'
    )

    for deleted_document in DeletedDocument.objects.all():
        task_trashed_document_delete.apply_async(
            kwargs={'trashed_document_id': deleted_document.pk}
        )


# Trashed document

@app.task(ignore_result=True)
def task_trashed_document_delete(trashed_document_id):
    DeletedDocument = apps.get_model(
        app_label='documents', model_name='DeletedDocument'
    )

    logger.debug(msg='Executing')
    deleted_document = DeletedDocument.objects.get(pk=trashed_document_id)
    deleted_document.delete()
    logger.debug(msg='Finshed')
