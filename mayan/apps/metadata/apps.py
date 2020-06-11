import logging

from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelFieldRelated, ModelProperty
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_multi_item, menu_object, menu_secondary,
    menu_setup
)
from mayan.apps.documents.signals import signal_post_document_type_change
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import DocumentMetadataHelper
from .events import (
    event_document_metadata_added, event_document_metadata_edited,
    event_document_metadata_removed, event_metadata_type_edited,
    event_metadata_type_relationship
)
from .handlers import (
    handler_index_document, handler_post_document_type_metadata_type_add,
    handler_post_document_type_metadata_type_delete,
    handler_post_document_type_change_metadata
)
from .html_widgets import widget_document_metadata
from .links import (
    link_metadata_add, link_metadata_edit, link_metadata_multiple_add,
    link_metadata_multiple_edit, link_metadata_multiple_remove,
    link_metadata_remove, link_metadata_view,
    link_setup_document_type_metadata_types, link_setup_metadata_type_create,
    link_setup_metadata_type_delete, link_setup_metadata_type_document_types,
    link_setup_metadata_type_edit, link_setup_metadata_type_list,
)
from .permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view,
    permission_metadata_type_delete, permission_metadata_type_edit,
    permission_metadata_type_view
)

from .search import metadata_type_search  # NOQA

logger = logging.getLogger(name=__name__)


class MetadataApp(MayanAppConfig):
    app_namespace = 'metadata'
    app_url = 'metadata'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.metadata'
    verbose_name = _('Metadata')

    def ready(self):
        super(MetadataApp, self).ready()

        from .wizard_steps import WizardStepMetadata  # NOQA

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        DocumentPageResult = apps.get_model(
            app_label='documents', model_name='DocumentPageResult'
        )

        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )

        DocumentMetadata = self.get_model(model_name='DocumentMetadata')
        DocumentTypeMetadataType = self.get_model(
            model_name='DocumentTypeMetadataType'
        )
        MetadataType = self.get_model(model_name='MetadataType')

        Document.add_to_class(
            name='metadata_value_of', value=DocumentMetadataHelper.constructor
        )

        EventModelRegistry.register(model=MetadataType)
        EventModelRegistry.register(model=DocumentTypeMetadataType)

        ModelProperty(
            model=Document, name='metadata_value_of.< metadata type name >',
            description=_(
                'Return the value of a specific document metadata.'
            ), label=_('Metadata value of')
        )

        ModelFieldRelated(
            model=Document, name='metadata__metadata_type__name',
            label=_('Metadata type name')
        )
        ModelFieldRelated(
            model=Document, name='metadata__value',
            label=_('Metadata type value')
        )

        ModelEventType.register(
            model=Document, event_types=(
                event_document_metadata_added,
                event_document_metadata_edited,
                event_document_metadata_removed,
            )
        )

        ModelEventType.register(
            model=MetadataType, event_types=(
                event_document_metadata_added,
                event_document_metadata_edited,
                event_document_metadata_removed,
                event_metadata_type_edited,
                event_metadata_type_relationship
            )
        )

        ModelEventType.register(
            model=DocumentType, event_types=(
                event_metadata_type_relationship,
            )
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_document_metadata_add,
                permission_document_metadata_edit,
                permission_document_metadata_remove,
                permission_document_metadata_view
            )
        )
        ModelPermission.register(
            model=MetadataType, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_document_metadata_add,
                permission_document_metadata_edit,
                permission_document_metadata_remove,
                permission_document_metadata_view, permission_events_view,
                permission_metadata_type_delete,
                permission_metadata_type_edit, permission_metadata_type_view
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentMetadata, related='metadata_type',
        )

        SourceColumn(
            source=Document, label=_('Metadata'),
            func=widget_document_metadata
        )

        SourceColumn(
            source=DocumentPageResult, label=_('Metadata'),
            func=widget_document_metadata
        )

        SourceColumn(
            attribute='metadata_type', is_identifier=True,
            is_sortable=True, source=DocumentMetadata
        )
        SourceColumn(
            attribute='value', include_label=True, is_sortable=True,
            source=DocumentMetadata
        )

        SourceColumn(
            attribute='is_required', include_label=True,
            source=DocumentMetadata, widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=MetadataType
        )
        SourceColumn(
            attribute='name', include_label=True, is_sortable=True,
            source=MetadataType
        )

        menu_facet.bind_links(links=(link_metadata_view,), sources=(Document,))
        menu_list_facet.bind_links(
            links=(link_setup_document_type_metadata_types,), sources=(
                DocumentType,
            )
        )
        menu_multi_item.bind_links(
            links=(
                link_metadata_multiple_add, link_metadata_multiple_edit,
                link_metadata_multiple_remove
            ), sources=(Document,)
        )
        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_setup_metadata_type_document_types,
                link_object_event_types_user_subcriptions_list,
                link_events_for_object,
            ), sources=(MetadataType,)
        )
        menu_object.bind_links(
            links=(
                link_setup_metadata_type_delete, link_setup_metadata_type_edit
            ), sources=(MetadataType,)
        )
        menu_secondary.bind_links(
            links=(
                link_setup_metadata_type_list,
                link_setup_metadata_type_create
            ), sources=(
                MetadataType, 'metadata:setup_metadata_type_list',
                'metadata:setup_metadata_type_create'
            )
        )
        menu_setup.bind_links(links=(link_setup_metadata_type_list,))
        menu_secondary.bind_links(
            links=(
                link_metadata_add, link_metadata_edit, link_metadata_remove
            ), sources=(
                'metadata:metadata_add', 'metadata:metadata_edit',
                'metadata:metadata_remove', 'metadata:metadata_view'
            )
        )

        post_delete.connect(
            dispatch_uid='metadata_handler_post_document_type_metadata_type_delete',
            receiver=handler_post_document_type_metadata_type_delete,
            sender=DocumentTypeMetadataType
        )
        post_save.connect(
            dispatch_uid='metadata_handler_post_document_type_metadata_type_add',
            receiver=handler_post_document_type_metadata_type_add,
            sender=DocumentTypeMetadataType
        )
        signal_post_document_type_change.connect(
            dispatch_uid='metadata_handler_post_document_type_change_metadata',
            receiver=handler_post_document_type_change_metadata,
            sender=Document
        )

        # Index updating

        post_delete.connect(
            dispatch_uid='metadata_handler_index_document_delete',
            receiver=handler_index_document,
            sender=DocumentMetadata
        )
        post_save.connect(
            dispatch_uid='metadata_handler_index_document_save',
            receiver=handler_index_document,
            sender=DocumentMetadata
        )
