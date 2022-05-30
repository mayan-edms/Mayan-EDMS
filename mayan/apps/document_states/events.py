from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Workflows'), name='document_states'
)

event_workflow_instance_created = namespace.add_event_type(
    label=_('Workflow instance created'), name='workflow_instance_created'
)
event_workflow_instance_transitioned = namespace.add_event_type(
    label=_('Workflow instance transitioned'),
    name='workflow_instance_transitioned'
)

event_workflow_template_created = namespace.add_event_type(
    label=_('Workflow created'), name='workflow_created'
)
event_workflow_template_edited = namespace.add_event_type(
    label=_('Workflow edited'), name='workflow_edited'
)
