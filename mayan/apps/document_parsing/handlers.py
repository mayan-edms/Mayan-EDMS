from __future__ import unicode_literals

import logging

from django.apps import apps

from mayan.apps.document_indexing.tasks import task_index_document

from .settings import setting_auto_parsing

logger = logging.getLogger(name=__name__)


def handler_index_document(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].document.pk)
    )


def handler_initialize_new_parsing_settings(sender, instance, **kwargs):
    DocumentTypeSettings = apps.get_model(
        app_label='document_parsing', model_name='DocumentTypeSettings'
    )

    if kwargs['created']:
        DocumentTypeSettings.objects.create(
            document_type=instance, auto_parsing=setting_auto_parsing.value
        )


def handler_parse_document_version(sender, instance, **kwargs):
    if instance.document.document_type.parsing_settings.auto_parsing:
        instance.submit_for_parsing()
