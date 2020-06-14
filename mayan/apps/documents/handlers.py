from django.apps import apps

from .literals import (
    DEFAULT_DOCUMENT_TYPE_LABEL, STORAGE_NAME_DOCUMENT_IMAGE
)
from .settings import setting_document_cache_maximum_size
from .signals import signal_post_initial_document_type
from .tasks import task_clean_empty_duplicate_lists, task_scan_duplicates_for


def handler_create_default_document_type(sender, **kwargs):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    if not DocumentType.objects.count():
        document_type = DocumentType.objects.create(
            label=DEFAULT_DOCUMENT_TYPE_LABEL
        )
        signal_post_initial_document_type.send(
            sender=DocumentType, instance=document_type
        )


def handler_create_document_cache(sender, **kwargs):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    Cache.objects.update_or_create(
        defaults={
            'maximum_size': setting_document_cache_maximum_size.value,
        }, defined_storage_name=STORAGE_NAME_DOCUMENT_IMAGE,
    )


def handler_scan_duplicates_for(sender, instance, **kwargs):
    task_scan_duplicates_for.apply_async(
        kwargs={'document_id': instance.document_id}
    )


def handler_remove_empty_duplicates_lists(sender, **kwargs):
    task_clean_empty_duplicate_lists.apply_async()
