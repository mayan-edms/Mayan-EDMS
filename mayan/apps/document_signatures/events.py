from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Document signatures'), name='document_signatures'
)

event_detached_signature_created = namespace.add_event_type(
    label=_('Detached signature created'), name='detached_signature_created'
)
event_detached_signature_uploaded = namespace.add_event_type(
    label=_('Detached signature uploaded'),
    name='detached_signature_uploaded'
)
event_embedded_signature_created = namespace.add_event_type(
    label=_('Embedded signature created'), name='embedded_signature_created'
)
