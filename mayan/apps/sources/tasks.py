import logging

from django.contrib.auth.models import User
from django.core.files import File

from mayan.celery import app

from common.models import SharedUploadedFile
from documents.models import DocumentType

from .models import Source

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_check_interval_source(source_id):
    source = Source.objects.get_subclass(pk=source_id)
    if source.enabled:
        source.check_source()


@app.task(ignore_result=True)
def task_source_upload_document(label, document_type_id, shared_uploaded_file_id, source_id, description=None, expand=False, language=None, metadata_dict_list=None, user_id=None):
    shared_uploaded_file = SharedUploadedFile.objects.get(pk=shared_uploaded_file_id)
    source = Source.objects.get_subclass(pk=source_id)
    document_type = DocumentType.objects.get(pk=document_type_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    with File(file=shared_uploaded_file.file) as file_object:
        source.upload_document(description=description, document_type=document_type, expand=expand, file_object=file_object, label=label, language=language, metadata_dict_list=metadata_dict_list, user=user)

    shared_uploaded_file.delete()

    # TODO: Report/record how was file uploaded
    #    if result['is_compressed'] is None:
    #        messages.success(request, _('File uploaded successfully.'))

    #    if result['is_compressed'] is True:
    #        messages.success(request, _('File uncompressed successfully and uploaded as individual files.'))

    #    if result['is_compressed'] is False:
    #        messages.warning(request, _('File was not a compressed file, uploaded as it was.'))
