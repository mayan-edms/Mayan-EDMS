from __future__ import unicode_literals

import logging

from django.apps import apps
from django.db import OperationalError
from django.utils.text import slugify

from mayan.celery import app

from mayan.apps.documents.literals import UPLOAD_NEW_DOCUMENT_RETRY_DELAY

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=UPLOAD_NEW_DOCUMENT_RETRY_DELAY, ignore_result=True)
def task_upload_new_document(self, document_type_id, shared_uploaded_file_id, extra_data=None):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    MetadataType = apps.get_model(
        app_label='metadata', model_name='MetadataType'
    )

    SharedUploadedFile = apps.get_model(
        app_label='common', model_name='SharedUploadedFile'
    )

    try:
        document_type = DocumentType.objects.get(pk=document_type_id)
        shared_file = SharedUploadedFile.objects.get(
            pk=shared_uploaded_file_id
        )
    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to retrieve shared data for '
            'new document of type: %s; %s. Retrying.', document_type, exception
        )
        raise self.retry(exc=exception)

    try:
        with shared_file.open() as file_object:
            new_document = document_type.new_document(file_object=file_object)
    except OperationalError as exception:
        logger.warning(
            'Operational error during attempt to create new document '
            'of type: %s; %s. Retrying.', document_type, exception
        )
        raise self.retry(exc=exception)
    except Exception as exception:
        # This except and else block emulate a finally:
        logger.error(
            'Unexpected error during attempt to create new document '
            'of type: %s; %s', document_type, exception
        )
        try:
            shared_file.delete()
        except OperationalError as exception:
            logger.warning(
                'Operational error during attempt to delete shared '
                'file: %s; %s.', shared_file, exception
            )
    else:
        if extra_data:
            for pair in extra_data.get('metadata_pairs', []):
                name = slugify(pair['name']).replace('-', '_')
                logger.debug(
                    'Metadata pair (label, name, value): %s, %s, %s',
                    pair['name'], name, pair['value']
                )

                metadata_type, created = MetadataType.objects.get_or_create(
                    name=name, defaults={'label': pair['name']}
                )
                if not new_document.document_type.metadata.filter(metadata_type=metadata_type).exists():
                    logger.debug('Metadata type created')
                    new_document.document_type.metadata.create(
                        metadata_type=metadata_type, required=False
                    )

                new_document.metadata.create(
                    metadata_type=metadata_type, value=pair['value']
                )

        try:
            shared_file.delete()
        except OperationalError as exception:
            logger.warning(
                'Operational error during attempt to delete shared '
                'file: %s; %s.', shared_file, exception
            )
