from django.db.models.signals import post_migrate
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import (
    permission_acl_edit, permission_acl_view
)
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary,
    menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import event_asset_edited
from .handlers import handler_create_asset_cache
from .links import (
    link_asset_create, link_asset_multiple_delete,
    link_asset_single_delete, link_asset_edit, link_asset_list,
    link_transformation_delete, link_transformation_edit,
    link_transformation_select
)
from .permissions import (
    permission_asset_delete, permission_asset_edit,
    permission_asset_view
)


class ConverterApp(MayanAppConfig):
    app_namespace = 'converter'
    app_url = 'converter'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.converter'
    verbose_name = _('Converter')

    def ready(self):
        super().ready()

        Asset = self.get_model(model_name='Asset')
        LayerTransformation = self.get_model(model_name='LayerTransformation')

        EventModelRegistry.register(model=Asset)

        ModelEventType.register(
            model=Asset, event_types=(
                event_asset_edited,
            )
        )

        ModelPermission.register(
            model=Asset, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_asset_delete, permission_asset_edit,
                permission_asset_view, permission_events_view
            )
        )

        ModelPermission.register_inheritance(
            model=LayerTransformation,
            related='object_layer__content_object',
        )

        SourceColumn(
            attribute='label', is_identifier=True,
            is_object_absolute_url=True, is_sortable=True, source=Asset
        )
        SourceColumn(
            attribute='internal_name', include_label=True,
            is_object_absolute_url=True, is_sortable=True, source=Asset
        )

        SourceColumn(
            attribute='order', is_identifier=True, is_sortable=True,
            source=LayerTransformation
        )
        SourceColumn(
            func=lambda context: force_text(s=context['object']),
            include_label=True, label=_('Transformation'),
            source=LayerTransformation
        )
        SourceColumn(
            attribute='arguments', include_label=True,
            source=LayerTransformation
        )

        menu_list_facet.bind_links(
            links=(link_acl_list,), sources=(Asset,)
        )

        menu_multi_item.bind_links(
            links=(link_asset_multiple_delete,), sources=(Asset,)
        )
        menu_object.bind_links(
            links=(
                link_asset_single_delete, link_asset_edit
            ), sources=(Asset,)
        )
        menu_secondary.bind_links(
            links=(link_asset_list, link_asset_create,),
            sources=(
                Asset, 'converter:asset_list', 'converter:asset_create',
                'converter:asset_multiple_delete',
            )
        )
        menu_setup.bind_links(
            links=(link_asset_list,)
        )

        menu_object.bind_links(
            links=(link_transformation_edit, link_transformation_delete),
            sources=(LayerTransformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_select,), sources=(LayerTransformation,)
        )
        menu_secondary.bind_links(
            links=(link_transformation_select,),
            sources=(
                'converter:transformation_create',
                'converter:transformation_list'
            )
        )

        post_migrate.connect(
            dispatch_uid='converter_handler_create_asset_cache',
            receiver=handler_create_asset_cache,
        )
