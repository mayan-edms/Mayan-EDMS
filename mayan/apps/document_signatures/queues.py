from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_signatures = CeleryQueue(
    label=_('Signatures'), name='signatures', worker=worker_medium
)

queue_signatures.add_task_type(
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_key_signatures',
    label=_('Verify key signatures')
)
queue_signatures.add_task_type(
    dotted_path='mayan.apps.document_signatures.tasks.task_unverify_key_signatures',
    label=_('Unverify key signatures')
)
queue_signatures.add_task_type(
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_document_version',
    label=_('Verify document version')
)

queue_tools.add_task_type(
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_missing_embedded_signature',
    label=_('Verify missing embedded signature')
)
