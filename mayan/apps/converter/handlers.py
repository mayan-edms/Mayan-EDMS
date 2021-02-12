from django.apps import apps

from .literals import STORAGE_NAME_ASSETS_CACHE
from .settings import setting_asset_cache_maximum_size


def handler_create_asset_cache(sender, **kwargs):
    Cache = apps.get_model(app_label='file_caching', model_name='Cache')
    Cache.objects.update_or_create(
        defaults={
            'maximum_size': setting_asset_cache_maximum_size.value,
        }, defined_storage_name=STORAGE_NAME_ASSETS_CACHE,
    )
