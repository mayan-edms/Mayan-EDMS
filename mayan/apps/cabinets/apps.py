from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.navigation.classes import SourceColumn

from .dependencies import *  # NOQA
from .events import (
    event_cabinet_edited, event_cabinet_add_document,
    event_cabinet_remove_document
)
from .links import (
    link_cabinet_list, link_document_cabinet_list,
    link_document_cabinet_remove, link_document_cabinet_add,
    link_document_multiple_cabinet_add, link_cabinet_child_add,
    link_cabinet_create, link_cabinet_delete, link_cabinet_edit,
    link_cabinet_view, link_custom_acl_list,
    link_multiple_document_cabinet_remove
)
from .menus import menu_cabinets
from .methods import method_get_document_cabinets
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_delete,
    permission_cabinet_edit, permission_cabinet_remove_document,
    permission_cabinet_view
)
from .widgets import widget_document_cabinets


class CabinetsApp(MayanAppConfig):
    app_namespace = 'cabinets'
    app_url = 'cabinets'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.cabinets'
    verbose_name = _('Cabinets')

    def ready(self):
        super(CabinetsApp, self).ready()
        from actstream import registry
        from .wizard_steps import WizardStepCabinets  # NOQA

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentCabinet = self.get_model(model_name='DocumentCabinet')
        Cabinet = self.get_model(model_name='Cabinet')

        # Add explicit order_by as DocumentCabinet ordering Meta option has no
        # effect.
        Document.add_to_class(
            name='document_cabinets', value=method_get_document_cabinets
        )

        ModelEventType.register(
            model=Cabinet, event_types=(
                event_cabinet_edited, event_cabinet_add_document,
                event_cabinet_remove_document
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_cabinet_add_document,
                permission_cabinet_remove_document,
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

        def get_root_filter():
            return {
                'acl_filter': {'level': 0},
                'acl_values': ('tree_id',),
                'field_lookup': 'tree_id__in'
            }

        ModelPermission.register_function(
            model=Cabinet, function=get_root_filter
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Cabinet
        )

        SourceColumn(
            source=Document, label=_('Cabinets'),
            func=lambda context: widget_document_cabinets(
                document=context['object'], user=context['request'].user
            ), order=1
        )

        document_page_search.add_model_field(
            field='document_version__document__cabinets__label',
            label=_('Cabinets')
        )
        document_search.add_model_field(
            field='cabinets__label', label=_('Cabinets')
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
                link_cabinet_view, link_custom_acl_list,
                link_events_for_object,
                link_object_event_types_user_subcriptions_list,
            ),
            sources=(Cabinet,)
        )

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
        menu_secondary.bind_links(
            links=(link_document_cabinet_add, link_document_cabinet_remove),
            sources=(
                'cabinets:document_cabinet_list',
                'cabinets:document_cabinet_add',
                'cabinets:document_cabinet_remove'
            )
        )

        registry.register(Cabinet)
