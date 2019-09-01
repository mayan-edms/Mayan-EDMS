from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from .literals import (
    CONTROL_SHEET_CODE_IMAGE_CACHE_NAME,
    CONTROL_SHEET_CODE_IMAGE_CACHE_STORAGE_INSTANCE_PATH
)
from .settings import setting_control_sheet_code_image_cache_maximum_size


def handler_create_control_sheet_codes_image_cache(sender, **kwargs):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    Cache.objects.update_or_create(
        defaults={
            'label': _('Control sheet codes'),
            'storage_instance_path': CONTROL_SHEET_CODE_IMAGE_CACHE_STORAGE_INSTANCE_PATH,
            'maximum_size': setting_control_sheet_code_image_cache_maximum_size.value,
        }, name=CONTROL_SHEET_CODE_IMAGE_CACHE_NAME,
    )


def handler_process_document_version(sender, instance, **kwargs):
    instance.submit_for_control_codes_processing()
