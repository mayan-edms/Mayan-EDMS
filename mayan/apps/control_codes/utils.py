from __future__ import unicode_literals

from django.apps import apps

from .literals import CONTROL_SHEET_CODE_IMAGE_CACHE_NAME


def callback_update_control_sheet_image_cache_size(setting):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    cache = Cache.objects.get(name=CONTROL_SHEET_CODE_IMAGE_CACHE_NAME)
    cache.maximum_size = setting.value
    cache.save()
