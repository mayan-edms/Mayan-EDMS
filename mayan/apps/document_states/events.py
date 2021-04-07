from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Workflows'), name='document_states'
)

event_workflow_template_created = namespace.add_event_type(
    label=_('Workflow created'), name='workflow_created'
)
event_workflow_template_edited = namespace.add_event_type(
    label=_('Workflow edited'), name='workflow_edited'
)
