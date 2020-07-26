from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import DEFAULT_TASK_RETRY_DELAY

namespace = SettingNamespace(
    label=_('Document indexing'), name='document_indexing',
)

setting_task_retry = namespace.add_setting(
    global_name='DOCUMENT_INDEXING_TASK_RETRY_DELAY',
    default=DEFAULT_TASK_RETRY_DELAY, help_text=_(
        'Amount of time in seconds, a failed indexing task will wait before '
        'retrying. Lower values will increase the speed at which documents '
        'are indexed but will cause a higher count of failed/retried tasks '
        'in the queue.'
    )
)
