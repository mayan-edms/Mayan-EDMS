import logging

from mayan.celery import app

from documents.exceptions import NewDocumentVersionNotAllowed
from documents.models import DocumentType

from .models import Source, StagingFolderSource

logger = logging.getLogger(__name__)


@app.task
def task_upload_document(source_id, file_object, filename=None, use_file_name=False, document_type_id=None, expand=False, metadata_dict_list=None, user=None, document_id=None, new_version_data=None, command_line=False, description=None, staging_file=None):
    source = Source.objects.get_subclass(pk=source_id)

    if document_type_id:
        document_type = DocumentType.objects.get(pk=document_type_id)
    else:
        document_type = None

    if document_id:
        document = Document.objects.get(pk=document_id)
    else:
        document = None

    #try:
    result = source.upload_file(file_object, filename, use_file_name, document_type, expand, metadata_dict_list, user, document, new_version_data, command_line, description)
    #except NewDocumentVersionNotAllowed:
    #    messages.error(request, _(u'New version uploads are not allowed for this document.'))

    #if not document:
        #    if result['is_compressed'] is None:
        #        messages.success(request, _(u'File uploaded successfully.'))

        #    if result['is_compressed'] is True:
        #        messages.success(request, _(u'File uncompressed successfully and uploaded as individual files.'))

        #    if result['is_compressed'] is False:
        #        messages.warning(request, _(u'File was not a compressed file, uploaded as it was.'))

    if isinstance(source, StagingFolderSource):
        if source.delete_after_upload:
            staging_file.delete()
