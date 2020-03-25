from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_WORKFLOW_CACHE
from .settings import (
    setting_workflowimagecache_storage,
    setting_workflowimagecache_storage_arguments,
)

storage_workflow_image = DefinedStorage(
    dotted_path=setting_workflowimagecache_storage.value,
    error_message=_(
        'Unable to initialize the workflow preview '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_workflowimagecache_storage.global_name,
            setting_workflowimagecache_storage_arguments.global_name
        )
    ),
    label=_('Workflow preview images'),
    name=STORAGE_NAME_WORKFLOW_CACHE,
    kwargs=setting_workflowimagecache_storage_arguments.value
)
