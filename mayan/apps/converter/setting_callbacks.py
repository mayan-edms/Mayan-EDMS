from django.apps import apps

from .literals import STORAGE_NAME_ASSETS_CACHE


def callback_update_asset_cache_size(setting):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    cache = Cache.objects.get(
        defined_storage_name=STORAGE_NAME_ASSETS_CACHE
    )
    cache.maximum_size = setting.value
    cache.save()
