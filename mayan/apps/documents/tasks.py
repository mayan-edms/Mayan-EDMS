import logging

from django.contrib.auth.models import User
from django.core.files import File

from mayan.celery import app

from .models import Document, DocumentType, DocumentVersion

logger = logging.getLogger(__name__)


@app.task
def task_get_document_image(document_id, *args, **kwargs):
    document = Document.objects.get(pk=document_id)
    return document.get_image(*args, **kwargs)


@app.task(ignore_result=True)
def task_clear_image_cache():
    # TODO: Error logging
    #try:
    Document.clear_image_cache()
    # except Exception as exception:
    #    messages.error(request, _(u'Error clearing document image cache; %s') % exception)


@app.task(ignore_result=True)
def task_update_page_count(version_id):
    document_version = DocumentVersion.objects.get(pk=version_id)
    document_version.update_page_count()


@app.task(ignore_result=True)
def task_new_document(document_type_id, file_path, label, description=None, expand=False, language=None, user_id=None):
    document_type = DocumentType.objects.get(pk=document_type_id)

    if user_id:
        user = User.objects.get(pk=user_id)
    else:
        user = None

    with File(file=open(file_path, mode='rb')) as file_object:
        new_version = Document.objects.new_document(document_type=document_type, expand=expand, file_object=file_object, label=label, description=description, language=language, user=user)

    # TODO: Report/record how was file uploaded
    #    if result['is_compressed'] is None:
    #        messages.success(request, _(u'File uploaded successfully.'))

    #    if result['is_compressed'] is True:
    #        messages.success(request, _(u'File uncompressed successfully and uploaded as individual files.'))

    #    if result['is_compressed'] is False:
    #        messages.warning(request, _(u'File was not a compressed file, uploaded as it was.'))
