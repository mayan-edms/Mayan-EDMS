from __future__ import unicode_literals

import logging

from django.apps import apps

from mayan.celery import app

from .classes import ControlCode

logger = logging.getLogger(__name__)


@app.task()
def task_generate_control_sheet_code_image(control_sheet_code_id):
    ControlSheetCode = apps.get_model(
        app_label='control_codes', model_name='ControlSheetCode'
    )

    control_sheet_code = ControlSheetCode.objects.get(pk=control_sheet_code_id)

    return control_sheet_code.generate_image()


@app.task(ignore_result=True)
def task_process_document_version(document_version_id):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(pk=document_version_id)

    ControlCode.process_document_version(
        document_version=document_version
    )
