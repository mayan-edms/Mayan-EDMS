import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_multi_item, menu_object, menu_tools, menu_user
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.navigation.classes import Separator

from .events import (
    event_user_impersonation_ended, event_user_impersonation_started,
    event_user_logged_in, event_user_logged_out
)
from .handlers import handler_user_logged_in, handler_user_logged_out
from .links import (
    link_logout, link_password_change, link_user_impersonate_form_start,
    link_user_impersonate_start, link_user_multiple_set_password,
    link_user_set_password
)
from .permissions import permission_users_impersonate

logger = logging.getLogger(name=__name__)


class AuthenticationApp(MayanAppConfig):
    app_namespace = 'authentication'
    app_url = 'authentication'
    has_tests = True
    name = 'mayan.apps.authentication'
    verbose_name = _('Authentication')

    def ready(self):
        super().ready()

        User = get_user_model()

        ModelEventType.register(
            model=User, event_types=(
                event_user_impersonation_ended,
                event_user_impersonation_started, event_user_logged_in,
                event_user_logged_out
            )
        )

        ModelPermission.register(
            model=User, permissions=(
                permission_users_impersonate,
            )
        )

        menu_multi_item.bind_links(
            links=(link_user_multiple_set_password,),
            sources=('user_management:user_list',)
        )

        menu_object.bind_links(
            links=(
                link_user_impersonate_start, link_user_set_password,
            ), sources=(User,)
        )

        menu_tools.bind_links(
            links=(link_user_impersonate_form_start,)
        )

        menu_user.bind_links(
            links=(
                Separator(), link_password_change, link_logout
            ), position=99
        )

        user_logged_in.connect(
            dispatch_uid='authentication_handler_user_logged_in',
            receiver=handler_user_logged_in,
            sender=User
        )
        user_logged_out.connect(
            dispatch_uid='authentication_handler_user_logged_out',
            receiver=handler_user_logged_out,
            sender=User
        )
