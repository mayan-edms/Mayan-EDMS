import logging

from django.contrib.auth.models import User
from django.db import OperationalError
from django.utils.translation import ugettext_lazy as _

from mayan.celery import app

from common.models import SharedUploadedFile
from converter.models import Transformation
from documents.models import DocumentType
from metadata.api import save_metadata_list

from .literals import DEFAULT_SOURCE_TASK_RETRY_DELAY
from .models import Source

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_check_interval_source(source_id):
    source = Source.objects.get_subclass(pk=source_id)
    if source.enabled:
        try:
            source.check_source()
        except Exception as exception:
            logger.error('Error processing source: %s; %s', source, exception)
            source.logs.create(message=_('Error processing source: %s') % exception)
        else:
            source.logs.all().delete()


@app.task(bind=True, default_retry_delay=DEFAULT_SOURCE_TASK_RETRY_DELAY, ignore_result=True)
def task_post_document_version_upload(self, source_id, document_version_id):
    try:
        source = Source.objects.get_subclass(pk=source_id)
        document_version = DocumentVersion.objects.get(pk=document_version_id)

        Transformation.objects.copy(source=Source.objects.get_subclass(pk=source_id), targets=document_version.pages.all())
    except OperationalError as exception:
        logger.warning('Operational error during post source document upload processing: %s. Retrying.', exception)
        raise self.retry(exc=exception)


@app.task(bind=True, default_retry_delay=DEFAULT_SOURCE_TASK_RETRY_DELAY, ignore_result=True)
def task_upload_document(self, document_type_id, shared_uploaded_file_id, label=None, language=None, user_id=None, description=None, metadata_dict_list=None):
    try:
        shared_uploaded_file = SharedUploadedFile.objects.get(pk=shared_uploaded_file_id)
        source = Source.objects.get_subclass(pk=source_id)
        document_type = DocumentType.objects.get(pk=document_type_id)

        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None

        if not label:
            label = shared_uploaded_file.filename

        with transaction.atomic():
            document = DocumentVersion.objects.create(document_type=document_type)

            document_version = document.new_document(
                file_object=file_object, label=label, description=description,
                language=language, _user=user
            )

            if metadata_dict_list:
                save_metadata_list(metadata_dict_list, document, create=True)

            task_post_source_document_version_upload.delay(source_id=source_id, document_version_id=document_version.pk, metadata_dict_list=metadata_dict_list)
    except OperationalError as exception:
        logger.warning('Operational error during attempt to handle source upload: %s. Retrying.', exception)
        raise self.retry(exc=exception)

    try:
        shared_uploaded_file.delete()
    except OperationalError as exception:
        logger.warning('Operational error during attempt to delete shared upload file: %s; %s. Retrying.', shared_uploaded_file, exception)


@app.task(bind=True, default_retry_delay=DEFAULT_SOURCE_TASK_RETRY_DELAY, ignore_result=True)
def task_source_handle_upload(self, label, document_type_id, shared_uploaded_file_id, source_id, description=None, expand=False, language=None, metadata_dict_list=None, user_id=None):
    try:
        shared_uploaded_file = SharedUploadedFile.objects.get(pk=shared_uploaded_file_id)
        source = Source.objects.get_subclass(pk=source_id)
        document_type = DocumentType.objects.get(pk=document_type_id)

        if user_id:
            user = User.objects.get(pk=user_id)
        else:
            user = None

        if not label:
            label = shared_uploaded_file.filename
    except OperationalError as exception:
        logger.warning('Operational error during attempt to load data to handle source upload: %s. Retrying.', exception)
        raise self.retry(exc=exception)

    with shared_uploaded_file.open() as file_object:
        source.handle_upload(description=description, document_type=document_type, expand=expand, file_object=file_object, label=label, language=language, metadata_dict_list=metadata_dict_list, user=user)

    try:
        shared_uploaded_file.delete()
    except OperationalError as exception:
        logger.warning('Operational error during attempt to delete shared upload file: %s; %s. Retrying.', shared_uploaded_file, exception)

    # TODO: Report/record how was file uploaded
    #    if result['is_compressed'] is None:
    #        messages.success(request, _('File uploaded successfully.'))

    #    if result['is_compressed'] is True:
    #        messages.success(request, _('File uncompressed successfully and uploaded as individual files.'))

    #    if result['is_compressed'] is False:
    #        messages.warning(request, _('File was not a compressed file, uploaded as it was.'))
