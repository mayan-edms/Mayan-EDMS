import logging

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_multi_item, menu_object, menu_tools, menu_user
)

logger = logging.getLogger(name=__name__)


class AuthenticationOTPApp(MayanAppConfig):
    app_namespace = 'authentication_otp'
    app_url = 'authentication_otp'
    has_tests = True
    name = 'mayan.apps.authentication_otp'
    verbose_name = _('Authentication OTP')
