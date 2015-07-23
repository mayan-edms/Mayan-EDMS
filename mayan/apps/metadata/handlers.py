from __future__ import unicode_literals

import logging

from .models import DocumentMetadata
from .tasks import task_add_required_metadata_type, task_remove_metadata_type

logger = logging.getLogger(__name__)


def post_document_type_metadata_type_add(sender, instance, created, **kwargs):
    logger.debug('instance: %s', instance)

    if created and instance.required:
        task_add_required_metadata_type.apply_async(
            kwargs={
                'document_type_id': instance.document_type.pk,
                'metadata_type_id': instance.metadata_type.pk
            }
        )


def post_document_type_metadata_type_delete(sender, instance, **kwargs):
    logger.debug('instance: %s', instance)
    task_remove_metadata_type.apply_async(
        kwargs={
            'document_type_id': instance.document_type.pk,
            'metadata_type_id': instance.metadata_type.pk
        }
    )


def post_post_document_type_change_metadata(sender, instance, **kwargs):
    logger.debug('received post_document_type_change')
    logger.debug('instance: %s', instance)
    # Delete existing document metadata
    for metadata in instance.metadata.all():
        metadata.delete(enforce_required=False)

    # Add new document type metadata types to document
    for document_type_metadata_type in instance.document_type.metadata.filter(required=True):
        DocumentMetadata.objects.create(
            document=instance,
            metadata_type=document_type_metadata_type.metadata_type,
            value=None
        )
