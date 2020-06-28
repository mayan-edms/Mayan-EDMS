from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

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

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        ResolvedSmartLink = self.get_model(model_name='ResolvedSmartLink')
        SmartLink = self.get_model(model_name='SmartLink')
        SmartLinkCondition = self.get_model(model_name='SmartLinkCondition')

        EventModelRegistry.register(model=SmartLink)

        ModelCopy(
            model=SmartLinkCondition
        ).add_fields(
            field_names=(
                'smart_link', 'inclusion', 'foreign_document_data', 'operator', 'expression',
                'negated', 'enabled',
            )
        )
        ModelCopy(
            model=SmartLink, bind_link=True, register_permission=True
        ).add_fields(
            field_names=(
                'label', 'dynamic_label', 'enabled', 'document_types',
                'conditions'
            ),
        )

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
        ModelPermission.register_inheritance(
            model=SmartLinkCondition, related='smart_link',
        )

        SourceColumn(
            func=lambda context: context['object'].get_label_for(
                document=context['document']
            ), is_identifier=True, label=_('Label'),
            source=ResolvedSmartLink
        )

        source_column_smart_link_label = SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=SmartLink
        )
        source_column_smart_link_label.add_exclude(ResolvedSmartLink)
        source_column_smart_link_dynamic_label = SourceColumn(
            attribute='dynamic_label', include_label=True, is_sortable=True,
            source=SmartLink
        )
        source_column_smart_link_dynamic_label.add_exclude(ResolvedSmartLink)
        source_column_smart_link_enabled = SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=SmartLink, widget=TwoStateWidget
        )
        source_column_smart_link_enabled.add_exclude(ResolvedSmartLink)
        SourceColumn(
            attribute='get_full_label', is_identifier=True,
            source=SmartLinkCondition
        )
        SourceColumn(
            attribute='enabled', include_label=True, is_sortable=True,
            source=SmartLinkCondition, widget=TwoStateWidget
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
        menu_object.unbind_links(
            links=(link_smart_link_delete, link_smart_link_edit,),
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
