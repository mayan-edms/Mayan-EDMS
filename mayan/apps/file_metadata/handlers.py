from __future__ import unicode_literals

from django.apps import apps

from mayan.apps.document_indexing.tasks import task_index_document

from .settings import setting_auto_process


def handler_index_document_version(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].document.pk)
    )


def handler_initialize_new_document_type_settings(sender, instance, **kwargs):
    DocumentTypeSettings = apps.get_model(
        app_label='file_metadata', model_name='DocumentTypeSettings'
    )

    if kwargs['created']:
        DocumentTypeSettings.objects.create(
            auto_process=setting_auto_process.value, document_type=instance
        )


def handler_process_document_version(sender, instance, **kwargs):
    if instance.document.document_type.file_metadata_settings.auto_process:
        instance.submit_for_file_metadata_processing()
