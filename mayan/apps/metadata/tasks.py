import logging

from mayan.celery import app

from documents.models import DocumentType

from .models import DocumentMetadata, MetadataType

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_remove_metadata_type(document_type_id, metadata_type_id):
    DocumentMetadata.objects.filter(
        document__document_type__id=document_type_id,
        metadata_type__id=metadata_type_id
    ).delete()


@app.task(ignore_result=True)
def task_add_required_metadata_type(document_type_id, metadata_type_id):
    metadata_type = MetadataType.objects.get(pk=metadata_type_id)

    for document in DocumentType.objects.get(pk=document_type_id).documents.all():
        document.metadata.create(metadata_type=metadata_type)
