import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_list_facet, menu_object
from mayan.apps.events.classes import ModelEventType

from .events import event_user_locale_profile_edited
from .handlers import handler_user_locale_profile_create
from .links import (
    link_user_locale_profile_detail, link_user_locale_profile_edit
)
from .patches import patchDjangoTranslation

logger = logging.getLogger(name=__name__)


class LocalesApp(MayanAppConfig):
    app_namespace = 'locales'
    app_url = 'locales'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.locales'
    verbose_name = _('Locales')

    def ready(self):
        super().ready()
        User = get_user_model()

        patchDjangoTranslation()

        ModelEventType.register(
            model=User, event_types=(
                event_user_locale_profile_edited,
            )
        )

        menu_list_facet.bind_links(
            links=(
                link_user_locale_profile_detail,
            ), sources=(User,)
        )

        menu_object.bind_links(
            links=(
                link_user_locale_profile_edit,
            ), sources=(User,)
        )

        post_save.connect(
            dispatch_uid='common_handler_user_locale_profile_create',
            receiver=handler_user_locale_profile_create,
            sender=settings.AUTH_USER_MODEL
        )
