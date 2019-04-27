from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.common.signals import perform_upgrade
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.events.permissions import permission_events_view

from .events import event_role_created, event_role_edited
from .handlers import handler_purge_permissions
from .links import (
    link_group_roles, link_role_create, link_role_delete, link_role_edit,
    link_role_groups, link_role_list, link_role_permissions
)
from .methods import method_group_roles_add, method_group_roles_remove
from .permissions import (
    permission_role_delete, permission_role_edit, permission_role_view
)
from .search import *  # NOQA


class PermissionsApp(MayanAppConfig):
    app_namespace = 'permissions'
    app_url = 'permissions'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.permissions'
    verbose_name = _('Permissions')

    def ready(self):
        super(PermissionsApp, self).ready()
        from actstream import registry

        Role = self.get_model('Role')
        Group = apps.get_model(app_label='auth', model_name='Group')

        Group.add_to_class(name='roles_add', value=method_group_roles_add)
        Group.add_to_class(name='roles_remove', value=method_group_roles_remove)

        ModelEventType.register(
            event_types=(event_role_created, event_role_edited), model=Role
        )

        ModelPermission.register(
            model=Role, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_role_delete,
                permission_role_edit, permission_role_view
            )
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_role_groups, link_role_permissions,
            ), sources=(Role,)
        )
        menu_list_facet.bind_links(
            links=(link_group_roles,), sources=(Group,)
        )
        menu_object.bind_links(
            links=(
                link_role_delete, link_role_edit
            ), sources=(Role,)
        )
        menu_secondary.bind_links(
            links=(link_role_list, link_role_create),
            sources=(Role, 'permissions:role_create', 'permissions:role_list')
        )
        menu_setup.bind_links(links=(link_role_list,))

        perform_upgrade.connect(
            dispatch_uid='permissions_handler_purge_permissions',
            receiver=handler_purge_permissions
        )

        registry.register(Role)
