from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_medium

queue_signatures = CeleryQueue(label=_('Signatures'), name='signatures', worker=worker_medium)

queue_signatures.add_task_type(
    label=_('Verify key signatures'),
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_key_signatures'
)
queue_signatures.add_task_type(
    label=_('Unverify key signatures'),
    dotted_path='mayan.apps.document_signatures.tasks.task_unverify_key_signatures'
)
queue_signatures.add_task_type(
    label=_('Verify document version'),
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_document_version'
)

queue_tools.add_task_type(
    label=_('Verify missing embedded signature'),
    dotted_path='mayan.apps.document_signatures.tasks.task_verify_missing_embedded_signature'
)
