import logging

from django.contrib.auth.models import User
from django.core.files import File

from mayan.celery import app

from documents.exceptions import NewDocumentVersionNotAllowed
from documents.models import Document, DocumentType

from .models import Source

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_check_interval_source(source_id):
    source = Source.objects.get_subclass(pk=source_id)
    if source.enabled:
        source.fetch_mail()


@app.task(ignore_result=True)
def task_upload_document(source_id, file_path, label, document_type_id, expand=False, metadata_dict_list=None, user_id=None, command_line=False, description=None, language=None):
    source = Source.objects.get_subclass(pk=source_id)
    document_type = DocumentType.objects.get(pk=document_type_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    with File(file=open(file_path, mode='rb')) as file_object:
        source.upload_document(file_object, label=label, document_type=document_type, expand=expand, metadata_dict_list=metadata_dict_list, user=user, command_line=command_line, description=description, language=language)

    # TODO: delete temporary_file

    # TODO: Report/record how was file uploaded
    #    if result['is_compressed'] is None:
    #        messages.success(request, _(u'File uploaded successfully.'))

    #    if result['is_compressed'] is True:
    #        messages.success(request, _(u'File uncompressed successfully and uploaded as individual files.'))

    #    if result['is_compressed'] is False:
    #        messages.warning(request, _(u'File was not a compressed file, uploaded as it was.'))


@app.task(ignore_result=True)
def task_upload_new_version(source_id, file_path, document_id, user_id, version_update=None, comment=None):
    source = Source.objects.get_subclass(pk=source_id)
    document = Document.objects.get(pk=document_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    # Use File class otherwise we get error:
    # 'file' object has no attribute '_committed'

    with File(file=open(file_path, mode='rb')) as file_object:
        document.new_version(file=file_object, user=user, version_update=version_update, comment=comment)
