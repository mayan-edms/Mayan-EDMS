from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Authentication OTP'), name='authentication_otp'
)

event_otp_disabled = namespace.add_event_type(
    label=_('OTP disabled'), name='otp_disabled'
)
event_otp_enabled = namespace.add_event_type(
    label=_('OTP enabled'), name='otp_enabled'
)
