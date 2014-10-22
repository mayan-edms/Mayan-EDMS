import logging

from mayan.celery import app

from .models import Document, DocumentVersion

logger = logging.getLogger(__name__)


@app.task
def task_get_document_image(document_id, *args, **kwargs):
    document = Document.objects.get(pk=document_id)
    return document.get_image(*args, **kwargs)


@app.task
def task_clear_image_cache():
    # TODO: Error logging
    #try:
    Document.clear_image_cache()
    # except Exception as exception:
    #    messages.error(request, _(u'Error clearing document image cache; %s') % exception)


@app.task
def task_update_page_count(version_id):
    document_version = DocumentVersion.objects.get(pk=version_id)
    document_version.update_page_count()
