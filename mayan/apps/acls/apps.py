from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_object, menu_secondary
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn

from .classes import ModelPermission
from .events import event_acl_created, event_acl_edited
from .links import link_acl_create, link_acl_delete, link_acl_permissions


class ACLsApp(MayanAppConfig):
    app_namespace = 'acls'
    app_url = 'acls'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.acls'
    verbose_name = _('ACLs')

    def ready(self):
        super(ACLsApp, self).ready()
        from actstream import registry

        AccessControlList = self.get_model(model_name='AccessControlList')

        ModelEventType.register(
            event_types=(event_acl_created, event_acl_edited),
            model=AccessControlList
        )

        ModelPermission.register_inheritance(
            model=AccessControlList, related='content_object',
        )

        SourceColumn(
            attribute='role', is_sortable=True, source=AccessControlList,
        )

        menu_object.bind_links(
            links=(
                link_acl_permissions, link_acl_delete,
                link_events_for_object,
                link_object_event_types_user_subcriptions_list
            ),
            sources=(AccessControlList,)
        )
        menu_secondary.bind_links(
            links=(link_acl_create,), sources=('acls:acl_list',)
        )

        registry.register(AccessControlList)
