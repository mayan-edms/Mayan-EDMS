import logging

from django.apps import apps

from mayan.apps.document_indexing.tasks import task_index_instance_document_add

from .tasks import task_add_required_metadata_type, task_remove_metadata_type

logger = logging.getLogger(name=__name__)


def handler_index_metadata_type_documents(sender, **kwargs):
    if not kwargs.get('created', False):
        for metadata in kwargs['instance'].documentmetadata_set.all():
            task_index_instance_document_add.apply_async(
                kwargs={'document_id': metadata.document.pk}
            )


def handler_post_document_type_change_metadata(sender, instance, **kwargs):
    logger.debug('received signal_post_document_type_change')
    logger.debug('instance: %s', instance)

    # Delete existing document metadata types not found in the new document
    # type

    # First get the existing metadata types not found in the new document
    # type
    unneeded_metadata = instance.metadata.exclude(
        metadata_type__in=instance.document_type.metadata.values(
            'metadata_type'
        )
    )

    # Remove the document metadata whose types are not found in the new
    # document type
    for metadata in unneeded_metadata:
        metadata.delete(enforce_required=False)

    DocumentMetadata = apps.get_model(
        app_label='metadata', model_name='DocumentMetadata'
    )

    # Add the metadata types of the new document type to the document
    # excluding existing document metadata
    # get_or_create is not used to avoid a possible triggering of indexes
    # or workflow on document change by metadata save signal
    new_document_type_metadata_types = instance.document_type.metadata.filter(
        required=True
    ).exclude(metadata_type__in=instance.metadata.values('metadata_type'))

    for document_type_metadata_type in new_document_type_metadata_types:
        DocumentMetadata.objects.create(
            document=instance,
            metadata_type=document_type_metadata_type.metadata_type,
            value=document_type_metadata_type.metadata_type.default
        )


def handler_post_document_type_metadata_type_add(sender, instance, created, **kwargs):
    logger.debug('instance: %s', instance)

    if created and instance.required:
        task_add_required_metadata_type.apply_async(
            kwargs={
                'document_type_id': instance.document_type.pk,
                'metadata_type_id': instance.metadata_type.pk
            }
        )


def handler_post_document_type_metadata_type_delete(sender, instance, **kwargs):
    logger.debug('instance: %s', instance)
    task_remove_metadata_type.apply_async(
        kwargs={
            'document_type_id': instance.document_type.pk,
            'metadata_type_id': instance.metadata_type.pk
        }
    )


def handler_pre_metadata_type_delete(sender, **kwargs):
    for metadata in kwargs['instance'].documentmetadata_set.all():
        # Remove each of the documents.
        # Trigger the remove event for each document so they can be
        # reindexed.
        metadata.delete()
