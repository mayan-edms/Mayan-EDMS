from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn

from .events import event_smart_link_edited
from .links import (
    link_document_type_smart_links, link_smart_link_create,
    link_smart_link_condition_create, link_smart_link_condition_delete,
    link_smart_link_condition_edit, link_smart_link_condition_list,
    link_smart_link_delete, link_smart_link_document_types,
    link_smart_link_edit, link_smart_link_instance_view,
    link_smart_link_instances_for_document, link_smart_link_list,
    link_smart_link_setup
)
from .permissions import (
    permission_smart_link_delete, permission_smart_link_edit,
    permission_smart_link_view
)


class LinkingApp(MayanAppConfig):
    app_namespace = 'linking'
    app_url = 'smart_links'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.linking'
    verbose_name = _('Linking')

    def ready(self):
        super(LinkingApp, self).ready()
        from actstream import registry

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        ResolvedSmartLink = self.get_model(model_name='ResolvedSmartLink')
        SmartLink = self.get_model(model_name='SmartLink')
        SmartLinkCondition = self.get_model(model_name='SmartLinkCondition')

        ModelEventType.register(
            event_types=(event_smart_link_edited,), model=SmartLink
        )

        ModelPermission.register(
            model=SmartLink, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_smart_link_delete, permission_smart_link_edit,
                permission_smart_link_view
            )
        )

        SourceColumn(
            source=ResolvedSmartLink, label=_('Label'),
            func=lambda context: context['object'].get_label_for(
                document=context['document']
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=SmartLink
        )
        SourceColumn(
            attribute='dynamic_label', is_sortable=True, source=SmartLink
        )
        SourceColumn(
            attribute='enabled', is_sortable=True, source=SmartLink,
            widget=TwoStateWidget
        )

        SourceColumn(
            attribute='get_full_label', is_identifier=True,
            source=SmartLinkCondition
        )
        SourceColumn(
            attribute='enabled', is_sortable=True, source=SmartLinkCondition,
            widget=TwoStateWidget
        )

        menu_facet.bind_links(
            links=(link_smart_link_instances_for_document,),
            sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_smart_link_document_types,
                link_object_event_types_user_subcriptions_list,
                link_smart_link_condition_list,
            ), sources=(SmartLink,)
        )
        menu_list_facet.bind_links(
            links=(link_document_type_smart_links,), sources=(DocumentType,)
        )
        menu_object.bind_links(
            links=(
                link_smart_link_condition_edit,
                link_smart_link_condition_delete
            ), sources=(SmartLinkCondition,)
        )
        menu_object.bind_links(
            links=(
                link_smart_link_delete, link_smart_link_edit
            ), sources=(SmartLink,)
        )
        menu_object.bind_links(
            links=(link_smart_link_instance_view,),
            sources=(ResolvedSmartLink,)
        )
        menu_secondary.bind_links(
            links=(link_smart_link_list, link_smart_link_create),
            sources=(
                SmartLink, 'linking:smart_link_list',
                'linking:smart_link_create'
            )
        )
        menu_secondary.bind_links(
            links=(link_smart_link_condition_create,),
            sources=(
                'linking:smart_link_condition_list',
                'linking:smart_link_condition_create',
                'linking:smart_link_condition_edit',
                'linking:smart_link_condition_delete'
            )
        )
        menu_setup.bind_links(links=(link_smart_link_setup,))

        registry.register(SmartLink)
