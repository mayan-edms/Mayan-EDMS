from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.events import EventTypeNamespace

namespace = EventTypeNamespace(name='mailing', label=_('Mailing'))

event_email_sent = namespace.add_event_type(
    name='email_send', label=_('Email sent')
)
