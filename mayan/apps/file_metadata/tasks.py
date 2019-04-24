from __future__ import unicode_literals

import logging

from django.apps import apps

from mayan.celery import app

from .classes import FileMetadataDriver

logger = logging.getLogger(__name__)


@app.task(ignore_result=True)
def task_process_document_version(document_version_id):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(pk=document_version_id)

    FileMetadataDriver.process_document_version(
        document_version=document_version
    )
