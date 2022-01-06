import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_secondary, menu_user
from mayan.apps.events.classes import ModelEventType

from .events import event_otp_disabled, event_otp_enabled
from .handlers import handler_initialize_new_user_otp_data
from .links import link_otp_detail, link_otp_disable, link_otp_enable

logger = logging.getLogger(name=__name__)


class AuthenticationOTPApp(MayanAppConfig):
    app_namespace = 'authentication_otp'
    app_url = 'authentication_otp'
    has_tests = True
    name = 'mayan.apps.authentication_otp'
    verbose_name = _('Authentication OTP')

    def ready(self):
        super().ready()

        User = get_user_model()

        ModelEventType.register(
            model=User, event_types=(
                event_otp_disabled, event_otp_enabled
            )
        )

        menu_secondary.bind_links(
            links=(link_otp_disable, link_otp_enable,), sources=(User,)
        )

        menu_user.bind_links(
            links=(
                link_otp_detail,
            )
        )

        post_save.connect(
            dispatch_uid='authentication_otp_handler_initialize_new_user_otp_data',
            receiver=handler_initialize_new_user_otp_data,
            sender=User
        )
