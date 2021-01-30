import logging

from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_user

from .handlers import (
    handler_user_locale_profile_session_config,
    handler_user_locale_profile_create
)
from .links import link_current_user_locale_profile_details, link_current_user_locale_profile_edit
from .patches import patchDjangoTranslation

logger = logging.getLogger(name=__name__)


class LocalesApp(MayanAppConfig):
    app_namespace = 'locales'
    app_url = 'locales'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.locales'
    verbose_name = _('Locales')

    def ready(self):
        super().ready()
        patchDjangoTranslation()

        menu_user.bind_links(
            links=(
                link_current_user_locale_profile_details, link_current_user_locale_profile_edit,
            ), position=50
        )

        post_save.connect(
            dispatch_uid='common_handler_user_locale_profile_create',
            receiver=handler_user_locale_profile_create,
            sender=settings.AUTH_USER_MODEL
        )

        user_logged_in.connect(
            dispatch_uid='common_handler_user_locale_profile_session_config',
            receiver=handler_user_locale_profile_session_config
        )
