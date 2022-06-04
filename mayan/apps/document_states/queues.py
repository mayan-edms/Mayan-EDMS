import datetime

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.queues import queue_tools
from mayan.apps.task_manager.classes import CeleryQueue
from mayan.apps.task_manager.workers import worker_b

from .settings import setting_workflow_state_escalation_check_interval

queue_document_states_medium = CeleryQueue(
    label=_('Document states medium'), name='document_states_medium',
    worker=worker_b
)

queue_document_states_medium.add_task_type(
    label=_('Launch a workflow for a document'),
    dotted_path='mayan.apps.document_states.tasks.task_launch_workflow_for'
)
queue_document_states_medium.add_task_type(
    label=_('Launch all workflows for a document'),
    dotted_path='mayan.apps.document_states.tasks.task_launch_all_workflow_for'
)
queue_document_states_medium.add_task_type(
    label=_('Check a workflow instance for state escalation.'),
    dotted_path='mayan.apps.document_states.tasks.task_workflow_instance_check_escalation'
)
queue_document_states_medium.add_task_type(
    label=_('Check all workflow instances for state escalation.'),
    dotted_path='mayan.apps.document_states.tasks.task_workflow_instance_check_escalation_all',
    schedule=datetime.timedelta(
        seconds=setting_workflow_state_escalation_check_interval.value
    )
)

queue_tools.add_task_type(
    label=_('Launch all workflows for all documents'),
    dotted_path='mayan.apps.document_states.tasks.task_launch_all_workflows'
)
queue_tools.add_task_type(
    label=_('Launch a workflow'),
    dotted_path='mayan.apps.document_states.tasks.task_launch_workflow'
)
