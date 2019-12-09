from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from .literals import (
    DEFAULT_DOCUMENT_TYPE_LABEL, DOCUMENT_CACHE_STORAGE_INSTANCE_PATH,
    DOCUMENT_IMAGES_CACHE_NAME
)
from .settings import setting_document_cache_maximum_size
from .signals import post_initial_document_type
from .tasks import task_clean_empty_duplicate_lists, task_scan_duplicates_for


def handler_create_default_document_type(sender, **kwargs):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )

    if not DocumentType.objects.count():
        document_type = DocumentType.objects.create(
            label=DEFAULT_DOCUMENT_TYPE_LABEL
        )
        post_initial_document_type.send(
            sender=DocumentType, instance=document_type
        )


def handler_create_document_cache(sender, **kwargs):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    Cache.objects.update_or_create(
        defaults={
            'label': _('Document images'),
            'storage_instance_path': DOCUMENT_CACHE_STORAGE_INSTANCE_PATH,
            'maximum_size': setting_document_cache_maximum_size.value,
        }, name=DOCUMENT_IMAGES_CACHE_NAME,
    )


def handler_scan_duplicates_for(sender, instance, **kwargs):
    task_scan_duplicates_for.apply_async(
        kwargs={'document_id': instance.document.pk}
    )


def handler_remove_empty_duplicates_lists(sender, **kwargs):
    task_clean_empty_duplicate_lists.apply_async()
