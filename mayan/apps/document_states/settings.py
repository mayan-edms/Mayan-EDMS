
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_GRAPHVIZ_DOT_PATH, DEFAULT_WORKFLOWS_IMAGE_CACHE_MAXIMUM_SIZE,
    DEFAULT_WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND,
    DEFAULT_WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS,
    DEFAULT_WORKFLOWS_IMAGE_CACHE_TIME
)
from .setting_callbacks import callback_update_workflow_image_cache_size

namespace = SettingNamespace(label=_('Workflows'), name='document_states')

setting_graphviz_dot_path = namespace.add_setting(
    default=DEFAULT_GRAPHVIZ_DOT_PATH,
    global_name='WORKFLOWS_GRAPHVIZ_DOT_PATH', help_text=_(
        'File path to the graphviz dot program used to generate workflow '
        'previews.'
    ), is_path=True
)
setting_workflow_image_cache_maximum_size = namespace.add_setting(
    default=DEFAULT_WORKFLOWS_IMAGE_CACHE_MAXIMUM_SIZE,
    global_name='WORKFLOWS_IMAGE_CACHE_MAXIMUM_SIZE',
    help_text=_(
        'The threshold at which the WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND '
        'will start deleting the oldest workflow image cache files. '
        'Specify the size in bytes.'
    ), post_edit_function=callback_update_workflow_image_cache_size
)
setting_workflow_image_cache_time = namespace.add_setting(
    default=DEFAULT_WORKFLOWS_IMAGE_CACHE_TIME,
    global_name='WORKFLOWS_IMAGE_CACHE_TIME',
    help_text=_(
        'Time in seconds that the browser should cache the supplied workflow '
        'images. The default of 31559626 seconds correspond to 1 year.'
    )
)
setting_workflow_image_cache_storage_backend = namespace.add_setting(
    default=DEFAULT_WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND,
    global_name='WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'workflow image files.'
    )
)
setting_workflow_image_cache_storage_backend_arguments = namespace.add_setting(
    default=DEFAULT_WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS,
    global_name='WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    help_text=_(
        'Arguments to pass to the WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND.'
    )
)
