from __future__ import unicode_literals

import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.navigation.classes import SourceColumn

from .links import (
    link_message_create, link_message_delete, link_message_edit,
    link_message_list
)
from .permissions import (
    permission_message_delete, permission_message_edit,
    permission_message_view
)

logger = logging.getLogger(__name__)


class MOTDApp(MayanAppConfig):
    app_namespace = 'motd'
    app_url = 'messages'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.motd'
    verbose_name = _('Message of the day')

    def ready(self):
        super(MOTDApp, self).ready()

        Message = self.get_model(model_name='Message')
        ModelPermission.register(
            model=Message, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_message_delete, permission_message_edit,
                permission_message_view
            )
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Message
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=Message, widget=TwoStateWidget
        )
        SourceColumn(
            attribute='start_datetime', empty_value=_('None'),
            include_label=True, is_sortable=True, source=Message
        )
        SourceColumn(
            attribute='end_datetime', empty_value=_('None'),
            include_label=True, is_sortable=True, source=Message
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list,
            ), sources=(Message,)
        )
        menu_object.bind_links(
            links=(
                link_message_delete, link_message_edit
            ), sources=(Message,)
        )
        menu_secondary.bind_links(
            links=(link_message_create,),
            sources=(Message, 'motd:message_list', 'motd:message_create')
        )
        menu_setup.bind_links(
            links=(link_message_list,)
        )
