from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.classes import ModelFieldRelated, ModelProperty
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.common.menus import (
    menu_facet, menu_list_facet, menu_multi_item, menu_object, menu_secondary,
    menu_setup
)
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.documents.signals import post_document_type_change
from mayan.apps.events.classes import ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.rest_api.fields import HyperlinkField
from mayan.apps.rest_api.serializers import LazyExtraFieldsSerializerMixin

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
from .methods import method_get_metadata
from .permissions import (
    permission_metadata_add, permission_metadata_edit,
    permission_metadata_remove, permission_metadata_view,
    permission_metadata_type_delete, permission_metadata_type_edit,
    permission_metadata_type_view
)

from .search import metadata_type_search  # NOQA

logger = logging.getLogger(__name__)


class MetadataApp(MayanAppConfig):
    app_namespace = 'metadata'
    app_url = 'metadata'
    has_rest_api = True
    has_tests = True
    name = 'mayan.apps.metadata'
    verbose_name = _('Metadata')

    def ready(self):
        super(MetadataApp, self).ready()
        from actstream import registry

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
            name='get_metadata', value=method_get_metadata
        )

        LazyExtraFieldsSerializerMixin.add_field(
            dotted_path='mayan.apps.documents.serializers.DocumentTypeSerializer',
            field_name='metadata_type_relation_list_url',
            field=HyperlinkField(
                lookup_url_kwarg='document_type_id',
                view_name='rest_api:document_type-metadata_type_relation-list'
            )
        )

        LazyExtraFieldsSerializerMixin.add_field(
            dotted_path='mayan.apps.documents.serializers.DocumentSerializer',
            field_name='metadata_list_url',
            field=HyperlinkField(
                lookup_url_kwarg='document_id',
                view_name='rest_api:document_metadata-list'
            )
        )

        #ModelAttribute(model=Document, name='get_metadata')

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
                permission_metadata_add, permission_metadata_edit,
                permission_metadata_remove, permission_metadata_view
            )
        )
        ModelPermission.register(
            model=MetadataType, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_metadata_add, permission_metadata_edit,
                permission_metadata_remove, permission_metadata_view,
                permission_events_view, permission_metadata_type_delete,
                permission_metadata_type_edit, permission_metadata_type_view
            )
        )
        ModelPermission.register_inheritance(
            model=DocumentMetadata, related='metadata_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeMetadataType, related='document_type',
        )
        ModelPermission.register_inheritance(
            model=DocumentTypeMetadataType, related='metadata_type',
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
            attribute='value', is_sortable=True, source=DocumentMetadata
        )

        SourceColumn(
            attribute='is_required', source=DocumentMetadata,
            widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=MetadataType
        )
        SourceColumn(attribute='name', is_sortable=True, source=MetadataType)

        document_search.add_model_field(
            field='metadata__metadata_type__name', label=_('Metadata type')
        )
        document_search.add_model_field(
            field='metadata__value', label=_('Metadata value')
        )

        document_page_search.add_model_field(
            field='document_version__document__metadata__metadata_type__name',
            label=_('Metadata type')
        )
        document_page_search.add_model_field(
            field='document_version__document__metadata__value',
            label=_('Metadata value')
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
        post_document_type_change.connect(
            dispatch_uid='metadata_handler_post_document_type_change_metadata',
            receiver=handler_post_document_type_change_metadata,
            sender=Document
        )
        post_save.connect(
            dispatch_uid='metadata_handler_post_document_type_metadata_type_add',
            receiver=handler_post_document_type_metadata_type_add,
            sender=DocumentTypeMetadataType
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

        registry.register(MetadataType)
        registry.register(DocumentTypeMetadataType)
