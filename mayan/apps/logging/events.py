from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Logging'), name='logging')

event_error_log_deleted = namespace.add_event_type(
    label=_('Error log deleted'), name='error_log_deleted'
)
