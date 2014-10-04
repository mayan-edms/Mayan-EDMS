import logging

from django.contrib.auth.models import User
from django.core.files import File

from mayan.celery import app

from documents.exceptions import NewDocumentVersionNotAllowed
from documents.models import DocumentType

from .models import Source

logger = logging.getLogger(__name__)


@app.task
def task_upload_document(source_id, file_path, filename=None, use_file_name=False, document_type_id=None, expand=False, metadata_dict_list=None, user_id=None, document_id=None, new_version_data=None, command_line=False, description=None):
    source = Source.objects.get_subclass(pk=source_id)

    if document_type_id:
        document_type = DocumentType.objects.get(pk=document_type_id)
    else:
        document_type = None

    if document_id:
        document = Document.objects.get(pk=document_id)
    else:
        document = None

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    with File(file=open(file_path, mode='rb')) as file_object:
        #try:
        result = source.upload_file(file_object, filename, use_file_name, document_type, expand, metadata_dict_list, user, document, new_version_data, command_line, description)
        #except NewDocumentVersionNotAllowed:
        #    messages.error(request, _(u'New version uploads are not allowed for this document.'))

    # TODO: delete temporary_file

    #if not document:
        #    if result['is_compressed'] is None:
        #        messages.success(request, _(u'File uploaded successfully.'))

        #    if result['is_compressed'] is True:
        #        messages.success(request, _(u'File uncompressed successfully and uploaded as individual files.'))

        #    if result['is_compressed'] is False:
        #        messages.warning(request, _(u'File was not a compressed file, uploaded as it was.'))


