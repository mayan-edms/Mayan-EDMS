from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(label=_('Mailing'), name='mailing')

event_email_sent = namespace.add_event_type(
    label=_('Email sent'), name='email_send'
)
