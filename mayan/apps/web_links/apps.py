from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .events import event_web_link_edited
from .links import (
    link_document_type_web_links, link_document_web_link_list,
    link_web_link_create, link_web_link_delete, link_web_link_document_types,
    link_web_link_edit, link_web_link_instance_view,
    link_web_link_list, link_web_link_setup
)
from .permissions import (
    permission_web_link_delete, permission_web_link_edit,
    permission_web_link_instance_view, permission_web_link_view
)


class WebLinksApp(MayanAppConfig):
    app_namespace = 'web_links'
    app_url = 'web_links'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.web_links'
    verbose_name = _('Links')

    def ready(self):
        super(WebLinksApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        ResolvedWebLink = self.get_model(model_name='ResolvedWebLink')
        WebLink = self.get_model(model_name='WebLink')

        EventModelRegistry.register(model=ResolvedWebLink)
        EventModelRegistry.register(model=WebLink)

        ModelEventType.register(
            event_types=(
                event_web_link_edited,
            ), model=WebLink
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_web_link_instance_view,
            )
        )
        ModelPermission.register(
            model=DocumentType, permissions=(
                permission_web_link_instance_view,
            )
        )
        ModelPermission.register(
            model=WebLink, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_web_link_delete, permission_web_link_edit,
                permission_web_link_instance_view, permission_web_link_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=ResolvedWebLink
        )
        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=WebLink
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=WebLink,
            widget=TwoStateWidget
        )

        menu_facet.bind_links(
            links=(link_document_web_link_list,),
            sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_web_link_document_types,
                link_object_event_types_user_subcriptions_list,
            ), sources=(WebLink,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_web_links,), sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(
                link_web_link_delete, link_web_link_edit
            ), sources=(WebLink,)
        )
        menu_object.bind_links(
            links=(link_web_link_instance_view,),
            sources=(ResolvedWebLink,)
        )
        menu_object.unbind_links(
            links=(
                link_web_link_delete, link_web_link_edit
            ), sources=(ResolvedWebLink,)
        )
        menu_secondary.bind_links(
            links=(link_web_link_list, link_web_link_create),
            sources=(
                WebLink, 'web_links:web_link_list',
                'web_links:web_link_create'
            )
        )
        menu_setup.bind_links(links=(link_web_link_setup,))
