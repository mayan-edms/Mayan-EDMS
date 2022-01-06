from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_otp_detail, icon_otp_disable, icon_otp_enable
from .utils import is_otp_backend_enabled


def condition_is_otp_backend_enabled(context, resolved_object):
    return is_otp_backend_enabled()


def condition_is_current_user(context, resolved_object):
    return condition_is_otp_backend_enabled(
        context=context, resolved_object=resolved_object
    ) and context['request'].user == resolved_object and not condition_otp_is_enabled(
        context=context, resolved_object=resolved_object
    )


def condition_otp_is_enabled(context, resolved_object):
    return condition_is_otp_backend_enabled(
        context=context, resolved_object=resolved_object
    ) and resolved_object.otp_data.is_enabled()


link_otp_detail = Link(
    condition=condition_is_otp_backend_enabled, icon=icon_otp_detail,
    text=_('OTP details'), view='authentication_otp:otp_detail'
)
link_otp_disable = Link(
    condition=condition_otp_is_enabled, icon=icon_otp_disable,
    text=_('Disable OTP'), view='authentication_otp:otp_disable'
)
link_otp_enable = Link(
    condition=condition_is_current_user, icon=icon_otp_enable,
    text=_('Enable OTP'), view='authentication_otp:otp_enable'
)
