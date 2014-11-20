import logging

from mayan.celery import app
from documents.models import Document

from .api import update_indexes, delete_indexes
from .tools import do_rebuild_all_indexes

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_delete_indexes(document_id):
    document = Document.objects.get(pk=document_id)
    delete_indexes(document)


@app.task(ignore_result=True)
def task_update_indexes(document_id):
    document = Document.objects.get(pk=document_id)
    update_indexes(document)


@app.task(ignore_result=True)
def task_do_rebuild_all_indexes():
    do_rebuild_all_indexes()
