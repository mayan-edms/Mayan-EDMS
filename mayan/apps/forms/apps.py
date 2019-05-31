from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_setup,
    menu_tools
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn

from .classes import FieldClass


class FormsApp(MayanAppConfig):
    app_namespace = 'forms'
    app_url = 'forms'
    #has_tests = True
    name = 'mayan.apps.forms'
    verbose_name = _('Forms')

    def ready(self):
        super(FormsApp, self).ready()
        FieldClass.initialize()
