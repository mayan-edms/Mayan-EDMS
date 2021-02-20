from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelCopy, ModelQueryFields
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import (
    event_cabinet_edited, event_cabinet_document_added,
    event_cabinet_document_removed
)
from .html_widgets import DocumentCabinetWidget
from .links import (
    link_cabinet_list, link_document_cabinet_list,
    link_document_cabinet_remove, link_document_cabinet_add,
    link_document_multiple_cabinet_add, link_cabinet_child_add,
    link_cabinet_create, link_cabinet_delete, link_cabinet_edit,
    link_cabinet_view, link_custom_acl_list,
    link_multiple_document_cabinet_remove
)
from .menus import menu_cabinets
from .methods import method_document_get_cabinets
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_delete,
    permission_cabinet_edit, permission_cabinet_remove_document,
    permission_cabinet_view
)


class CabinetsApp(MayanAppConfig):
    app_namespace = 'cabinets'
    app_url = 'cabinets'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.cabinets'
    static_media_ignore_patterns = (
        'cabinets/node_modules/jstree/component.json',
        'cabinets/node_modules/jstree/jstree.jquery.json',
        'cabinets/node_modules/jstree/src/*',
    )
    verbose_name = _('Cabinets')

    def ready(self):
        super().ready()

        Cabinet = self.get_model(model_name='Cabinet')
        CabinetSearchResult = self.get_model(model_name='CabinetSearchResult')
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentCabinet = self.get_model(model_name='DocumentCabinet')
        DocumentFileSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentFileSearchResult'
        )
        DocumentFilePageSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentFilePageSearchResult'
        )
        DocumentVersionSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentVersionSearchResult'
        )
        DocumentVersionPageSearchResult = apps.get_model(
            app_label='documents', model_name='DocumentVersionPageSearchResult'
        )

        # Add explicit order_by as DocumentCabinet ordering Meta option has no
        # effect.
        Document.add_to_class(
            name='get_cabinets', value=method_document_get_cabinets
        )

        EventModelRegistry.register(model=Cabinet)

        def cabinet_model_copy_condition(instance):
            return instance.is_root_node()

        def cabinet_unique_conditional(instance, new_instance_dictionary):
            if instance.parent:
                return instance.parent_id == new_instance_dictionary['parent_id'] and instance.label == new_instance_dictionary['label']
            else:
                return not new_instance_dictionary['parent_id'] and instance.label == new_instance_dictionary['label']

        ModelCopy(
            model=Cabinet, condition=cabinet_model_copy_condition,
            bind_link=True, register_permission=True
        ).add_fields(
            field_names=('label', 'documents'), unique_conditional={
                'label': cabinet_unique_conditional
            }
        )

        ModelEventType.register(
            model=Cabinet, event_types=(
                event_cabinet_edited, event_cabinet_document_added,
                event_cabinet_document_removed
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_cabinet_add_document,
                permission_cabinet_remove_document, permission_cabinet_view,
                permission_events_view
            )
        )

        ModelPermission.register(
            model=Cabinet, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cabinet_delete, permission_cabinet_edit,
                permission_cabinet_view, permission_cabinet_add_document,
                permission_cabinet_remove_document
            )
        )

        model_query_fields_document = ModelQueryFields(model=Document)
        model_query_fields_document.add_prefetch_related_field(field_name='cabinets')

        def get_root_filter():
            return {
                'acl_filter': {'level': 0},
                'acl_values': ('tree_id',),
                'field_lookup': 'tree_id__in'
            }

        ModelPermission.register_field_query_function(
            model=Cabinet, function=get_root_filter
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Cabinet
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=CabinetSearchResult
        )
        SourceColumn(
            attribute='get_full_path', source=CabinetSearchResult
        )

        SourceColumn(
            label=_('Cabinets'), order=1, source=Document,
            widget=DocumentCabinetWidget
        )
        SourceColumn(
            attribute='document', label=_('Cabinets'), order=1,
            source=DocumentFileSearchResult, widget=DocumentCabinetWidget
        )
        SourceColumn(
            attribute='document_file__document', label=_('Cabinets'), order=1,
            source=DocumentFilePageSearchResult, widget=DocumentCabinetWidget
        )
        SourceColumn(
            attribute='document', label=_('Cabinets'), order=1,
            source=DocumentVersionSearchResult, widget=DocumentCabinetWidget
        )
        SourceColumn(
            attribute='document_version__document', label=_('Cabinets'),
            order=1, source=DocumentVersionPageSearchResult,
            widget=DocumentCabinetWidget
        )

        menu_facet.bind_links(
            links=(link_document_cabinet_list,), sources=(Document,)
        )

        menu_cabinets.bind_links(
            links=(
                link_cabinet_list, link_cabinet_create
            )
        )
        menu_list_facet.bind_links(
            links=(
                link_cabinet_view, link_custom_acl_list
            ),
            sources=(Cabinet,)
        )
        menu_list_facet.add_proxy_inclusions(source=CabinetSearchResult)

        menu_main.bind_links(links=(menu_cabinets,), position=98)

        menu_multi_item.bind_links(
            links=(
                link_document_multiple_cabinet_add,
                link_multiple_document_cabinet_remove
            ), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_cabinet_view,
            ), sources=(DocumentCabinet, )
        )
        menu_object.bind_links(
            links=(
                link_cabinet_delete, link_cabinet_edit, link_cabinet_child_add
            ), sources=(Cabinet,)
        )
        menu_object.add_proxy_inclusions(source=CabinetSearchResult)
        menu_object.unbind_links(
            links=(
                link_cabinet_delete, link_cabinet_edit, link_cabinet_child_add
            ), sources=(DocumentCabinet,)
        )
        menu_secondary.bind_links(
            links=(link_document_cabinet_add, link_document_cabinet_remove),
            sources=(
                'cabinets:document_cabinet_list',
                'cabinets:document_cabinet_add',
                'cabinets:document_cabinet_remove'
            )
        )
