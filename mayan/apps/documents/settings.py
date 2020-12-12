from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_DOCUMENTS_CACHE_MAXIMUM_SIZE,
    DEFAULT_DOCUMENTS_CACHE_STORAGE_BACKEND,
    DEFAULT_DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_DOCUMENTS_DISPLAY_HEIGHT, DEFAULT_DOCUMENTS_DISPLAY_WIDTH,
    DEFAULT_DOCUMENTS_FAVORITE_COUNT, DEFAULT_DOCUMENTS_HASH_BLOCK_SIZE,
    DEFAULT_DOCUMENTS_LIST_THUMBNAIL_WIDTH,
    DEFAULT_DOCUMENTS_PAGE_IMAGE_CACHE_TIME, DEFAULT_DOCUMENTS_PREVIEW_HEIGHT,
    DEFAULT_DOCUMENTS_PREVIEW_WIDTH, DEFAULT_DOCUMENTS_PRINT_HEIGHT,
    DEFAULT_DOCUMENTS_PRINT_WIDTH, DEFAULT_DOCUMENTS_RECENT_ACCESS_COUNT,
    DEFAULT_DOCUMENTS_RECENT_ADDED_COUNT, DEFAULT_DOCUMENTS_ROTATION_STEP,
    DEFAULT_DOCUMENTS_STORAGE_BACKEND,
    DEFAULT_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_DOCUMENTS_THUMBNAIL_HEIGHT, DEFAULT_DOCUMENTS_THUMBNAIL_WIDTH,
    DEFAULT_DOCUMENTS_ZOOM_MAX_LEVEL, DEFAULT_DOCUMENTS_ZOOM_MIN_LEVEL,
    DEFAULT_DOCUMENTS_ZOOM_PERCENT_STEP, DEFAULT_LANGUAGE,
    DEFAULT_LANGUAGE_CODES, DEFAULT_STUB_EXPIRATION_INTERVAL,
    DEFAULT_TASK_GENERATE_DOCUMENT_PAGE_IMAGE_RETRY_DELAY
)
from .setting_callbacks import callback_update_cache_size
from .setting_migrations import DocumentsSettingMigration

namespace = SettingNamespace(
    label=_('Documents'), migration_class=DocumentsSettingMigration,
    name='documents', version='0002'
)

setting_document_cache_maximum_size = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_CACHE_MAXIMUM_SIZE,
    global_name='DOCUMENTS_CACHE_MAXIMUM_SIZE', help_text=_(
        'The threshold at which the DOCUMENT_CACHE_STORAGE_BACKEND will start '
        'deleting the oldest document image cache files. Specify the size in '
        'bytes.'
    ), post_edit_function=callback_update_cache_size
)
setting_documentimagecache_storage = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_CACHE_STORAGE_BACKEND,
    global_name='DOCUMENTS_CACHE_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'document image files.'
    )
)
setting_documentimagecache_storage_arguments = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS,
    global_name='DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the DOCUMENT_CACHE_STORAGE_BACKEND.'
    ),
)
setting_display_height = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_DISPLAY_HEIGHT,
    global_name='DOCUMENTS_DISPLAY_HEIGHT'
)
setting_display_width = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_DISPLAY_WIDTH,
    global_name='DOCUMENTS_DISPLAY_WIDTH'
)
setting_favorite_count = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_FAVORITE_COUNT,
    global_name='DOCUMENTS_FAVORITE_COUNT', help_text=_(
        'Maximum number of favorite documents to remember per user.'
    )
)
setting_fix_orientation = namespace.add_setting(
    default=False, global_name='DOCUMENTS_FIX_ORIENTATION', help_text=_(
        'Detect the orientation of each of the document\'s pages '
        'and create a corresponding rotation transformation to '
        'display it rightside up. This is an experimental '
        'feature and it is disabled by default.'
    )
)
setting_hash_block_size = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_HASH_BLOCK_SIZE,
    global_name='DOCUMENTS_HASH_BLOCK_SIZE', help_text=_(
        'Size of blocks to use when calculating the document file\'s '
        'checksum. A value of 0 disables the block calculation and the entire '
        'file will be loaded into memory.'
    )
)
setting_language = namespace.add_setting(
    default=DEFAULT_LANGUAGE, global_name='DOCUMENTS_LANGUAGE',
    help_text=_('Default documents language (in ISO639-3 format).')
)
setting_language_codes = namespace.add_setting(
    default=DEFAULT_LANGUAGE_CODES, global_name='DOCUMENTS_LANGUAGE_CODES',
    help_text=_('List of supported document languages. In ISO639-3 format.')
)
settings_document_page_image_cache_time = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_PAGE_IMAGE_CACHE_TIME,
    global_name='DOCUMENTS_PAGE_IMAGE_CACHE_TIME', help_text=_(
        'Time in seconds that the browser should cache the supplied document '
        'images. The default of 31559626 seconds corresponde to 1 year.'
    )
)
setting_preview_height = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_PREVIEW_HEIGHT,
    global_name='DOCUMENTS_PREVIEW_HEIGHT'
)
setting_preview_width = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_PREVIEW_WIDTH,
    global_name='DOCUMENTS_PREVIEW_WIDTH'
)
setting_print_height = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_PRINT_HEIGHT,
    global_name='DOCUMENTS_PRINT_HEIGHT'
)
setting_print_width = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_PRINT_WIDTH,
    global_name='DOCUMENTS_PRINT_WIDTH'
)
setting_recent_access_count = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_RECENT_ACCESS_COUNT,
    global_name='DOCUMENTS_RECENT_ACCESS_COUNT', help_text=_(
        'Maximum number of recently accessed (created, edited, viewed) '
        'documents to remember per user.'
    )
)
setting_recent_added_count = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_RECENT_ADDED_COUNT,
    global_name='DOCUMENTS_RECENT_ADDED_COUNT', help_text=_(
        'Maximum number of recently created documents to show.'
    )
)
setting_rotation_step = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_ROTATION_STEP,
    global_name='DOCUMENTS_ROTATION_STEP', help_text=_(
        'Amount in degrees to rotate a document page per user interaction.'
    )
)
setting_storage_backend = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_STORAGE_BACKEND,
    global_name='DOCUMENTS_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing document '
        'files.'
    )
)
setting_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS,
    global_name='DOCUMENTS_STORAGE_BACKEND_ARGUMENTS', help_text=_(
        'Arguments to pass to the DOCUMENT_STORAGE_BACKEND.'
    )
)
setting_stub_expiration_interval = namespace.add_setting(
    default=DEFAULT_STUB_EXPIRATION_INTERVAL,
    global_name='DOCUMENTS_STUB_EXPIRATION_INTERVAL', help_text=_(
        'Time after which a document stub will be considered invalid and '
        'deleted.'
    )
)
setting_task_generate_document_page_image_retry_delay = namespace.add_setting(
    default=DEFAULT_TASK_GENERATE_DOCUMENT_PAGE_IMAGE_RETRY_DELAY,
    global_name='DOCUMENT_TASK_GENERATE_DOCUMENT_PAGE_IMAGE_RETRY_DELAY',
    help_text=_(
        'Amount of time in seconds, a failed document page image task will '
        'wait before retrying.'
    )
)
setting_thumbnail_height = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_THUMBNAIL_HEIGHT,
    global_name='DOCUMENTS_THUMBNAIL_HEIGHT', help_text=_(
        'Height in pixels of the document thumbnail image.'
    )
)
setting_thumbnail_width = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_THUMBNAIL_WIDTH,
    global_name='DOCUMENTS_THUMBNAIL_WIDTH', help_text=(
        'Width in pixels of the document thumbnail image.'
    )
)
setting_list_thumbnail_width = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_LIST_THUMBNAIL_WIDTH,
    global_name='DOCUMENTS_LIST_THUMBNAIL_WIDTH', help_text=(
        'Width in pixels of the document thumbnail image when shown in list '
        'view mode.'
    )
)
setting_zoom_max_level = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_ZOOM_MAX_LEVEL,
    global_name='DOCUMENTS_ZOOM_MAX_LEVEL', help_text=_(
        'Maximum amount in percent (%) to allow user to zoom in a document '
        'page interactively.'
    )
)
setting_zoom_min_level = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_ZOOM_MIN_LEVEL,
    global_name='DOCUMENTS_ZOOM_MIN_LEVEL', help_text=_(
        'Minimum amount in percent (%) to allow user to zoom out a document '
        'page interactively.'
    )
)
setting_zoom_percent_step = namespace.add_setting(
    default=DEFAULT_DOCUMENTS_ZOOM_PERCENT_STEP,
    global_name='DOCUMENTS_ZOOM_PERCENT_STEP', help_text=_(
        'Amount in percent zoom in or out a document page per user '
        'interaction.'
    )
)
