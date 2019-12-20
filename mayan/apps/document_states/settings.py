from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .literals import DEFAULT_WORKFLOW_IMAGE_CACHE_MAXIMUM_SIZE
from .utils import callback_update_workflow_image_cache_size

namespace = Namespace(label=_('Workflows'), name='document_states')

setting_workflow_image_cache_maximum_size = namespace.add_setting(
    global_name='WORKFLOWS_IMAGE_CACHE_MAXIMUM_SIZE',
    default=DEFAULT_WORKFLOW_IMAGE_CACHE_MAXIMUM_SIZE,
    help_text=_(
        'The threshold at which the WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND will '
        'start deleting the oldest workflow image cache files. Specify the '
        'size in bytes.'
    ), post_edit_function=callback_update_workflow_image_cache_size
)
settings_workflow_image_cache_time = namespace.add_setting(
    global_name='WORKFLOWS_IMAGE_CACHE_TIME', default='31556926',
    help_text=_(
        'Time in seconds that the browser should cache the supplied workflow '
        'images. The default of 31559626 seconds corresponde to 1 year.'
    )
)
setting_workflowimagecache_storage = namespace.add_setting(
    global_name='WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'workflow image files.'
    )
)
setting_workflowimagecache_storage_arguments = namespace.add_setting(
    global_name='WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default={'location': os.path.join(settings.MEDIA_ROOT, 'workflows')},
    help_text=_(
        'Arguments to pass to the WORKFLOWS_IMAGE_CACHE_STORAGE_BACKEND.'
    )
)
