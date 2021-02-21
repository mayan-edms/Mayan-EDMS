from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import menu_object, menu_secondary, menu_setup
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import ObjectLinkWidget

from .classes import ModelPermission
from .events import event_acl_deleted, event_acl_edited
from .links import (
    link_acl_create, link_acl_delete, link_acl_permissions,
    link_global_acl_list
)


class ACLsApp(MayanAppConfig):
    app_namespace = 'acls'
    app_url = 'acls'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.acls'
    verbose_name = _('ACLs')

    def ready(self):
        super().ready()

        AccessControlList = self.get_model(model_name='AccessControlList')
        GlobalAccessControlListProxy = self.get_model(
            model_name='GlobalAccessControlListProxy'
        )

        EventModelRegistry.register(model=AccessControlList, menu=menu_object)

        ModelCopy(model=AccessControlList).add_fields(
            field_names=(
                'content_object', 'permissions', 'role'
            )
        )

        ModelEventType.register(
            event_types=(
                event_acl_deleted, event_acl_edited
            ), model=AccessControlList
        )

        ModelPermission.register_inheritance(
            model=AccessControlList, related='content_object',
        )

        SourceColumn(
            attribute='role', is_sortable=True, source=AccessControlList
        )

        SourceColumn(
            attribute='content_object',
            is_identifier=True,
            help_text=_(
                'Object for which the access is granted. When sorting '
                'objects, only the type is used and not the actual label of '
                'the object.'
            ), include_label=True, is_sortable=True, label=_('Object'),
            sort_field='content_type', source=GlobalAccessControlListProxy,
            widget=ObjectLinkWidget
        )

        menu_object.bind_links(
            links=(
                link_acl_permissions, link_acl_delete
            ), sources=(AccessControlList, GlobalAccessControlListProxy)
        )
        menu_secondary.bind_links(
            links=(link_acl_create,), sources=('acls:acl_list',)
        )
        menu_setup.bind_links(
            links=(link_global_acl_list,)
        )
