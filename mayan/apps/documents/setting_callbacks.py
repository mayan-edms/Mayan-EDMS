import logging

from django.apps import apps

from .literals import STORAGE_NAME_DOCUMENT_IMAGE

logger = logging.getLogger(name=__name__)


def callback_update_cache_size(setting):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    cache = Cache.objects.get(
        defined_storage_name=STORAGE_NAME_DOCUMENT_IMAGE
    )
    cache.maximum_size = setting.value
    cache.save()
