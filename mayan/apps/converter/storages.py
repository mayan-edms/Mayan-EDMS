from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_ASSETS, STORAGE_NAME_ASSETS_CACHE
from .settings import (
    setting_asset_cache_storage_backend,
    setting_asset_cache_storage_backend_arguments,
    setting_asset_storage_backend, setting_asset_storage_backend_arguments
)

storage_assets = DefinedStorage(
    dotted_path=setting_asset_storage_backend.value,
    error_message=_(
        'Unable to initialize the converter asset '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_asset_storage_backend.global_name,
            setting_asset_storage_backend_arguments.global_name
        )
    ), label=_('Assets'), name=STORAGE_NAME_ASSETS,
    kwargs=setting_asset_storage_backend_arguments.value
)

storage_assets_cache = DefinedStorage(
    dotted_path=setting_asset_cache_storage_backend.value,
    error_message=_(
        'Unable to initialize the converter asset cache'
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_asset_cache_storage_backend.global_name,
            setting_asset_cache_storage_backend_arguments.global_name
        )
    ), label=_('Assets cache'), name=STORAGE_NAME_ASSETS_CACHE,
    kwargs=setting_asset_cache_storage_backend_arguments.value
)
