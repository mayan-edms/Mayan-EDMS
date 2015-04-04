from __future__ import absolute_import, unicode_literals

import tempfile

from django import apps
from django.utils.translation import ugettext_lazy as _

from actstream import registry

from acls.api import class_permissions
from common.classes import ModelAttribute
from common import menu_facet, menu_object, menu_setup
from common.utils import encapsulate, validate_path
from dynamic_search.classes import SearchModel
from events.permissions import PERMISSION_EVENTS_VIEW
from main import FrontPageButton, MissingItem
from main.api import register_maintenance_links
from navigation.api import register_model_list_columns
from rest_api.classes import APIEndPoint
from statistics.classes import StatisticNamespace

from documents import settings as document_settings
from .links import (
    link_clear_image_cache, link_document_clear_transformations,
    link_document_content, link_document_delete, link_document_document_type_edit,
    link_document_events_view, document_multiple_document_type_edit,
    link_document_download, link_document_edit, link_document_list, link_document_list_recent,
    document_multiple_delete, document_multiple_clear_transformations,
    document_multiple_download, document_multiple_update_page_count,
    document_page_edit, document_page_navigation_first,
    document_page_navigation_last, document_page_navigation_next,
    document_page_navigation_previous, document_page_rotate_left,
    document_page_rotate_right, document_page_text,
    document_page_transformation_list, document_page_transformation_create,
    document_page_transformation_edit, document_page_transformation_delete,
    document_page_view, document_page_view_reset, document_page_zoom_in,
    document_page_zoom_out, link_document_preview, link_document_print,
    link_document_properties, document_type_create, document_type_delete,
    document_type_edit, document_type_filename_create,
    document_type_filename_delete, document_type_filename_edit,
    document_type_filename_list, document_type_list, link_document_type_setup,
    link_document_update_page_count, document_version_download,
    link_document_version_list, document_version_revert
)
from .models import (
    Document, DocumentPage, DocumentPageTransformation, DocumentType,
    DocumentTypeFilename, DocumentVersion
)
from .permissions import (
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
    PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_NEW_VERSION,
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_TRANSFORM,
    PERMISSION_DOCUMENT_VERSION_REVERT, PERMISSION_DOCUMENT_VIEW
)
from .settings import THUMBNAIL_SIZE
from .statistics import DocumentStatistics, DocumentUsageStatistics
from .widgets import document_thumbnail


class DocumentsApp(apps.AppConfig):
    name = 'documents'
    verbose_name = _('Documents')

    def ready(self):
        # Document type links
        #register_links(DocumentType, [document_type_edit, document_type_filename_list, document_type_delete])
        #register_links([DocumentType, 'documents:document_type_create', 'documents:document_type_list'], [document_type_list, document_type_create], menu_name='secondary_menu')
        #register_links(DocumentTypeFilename, [document_type_filename_edit, document_type_filename_delete])
        #register_links([DocumentTypeFilename, 'documents:document_type_filename_list', 'documents:document_type_filename_create'], [document_type_filename_create], menu_name='sidebar')

        # Register document facet links
        menu_facet.bind_links(links=[link_document_preview], sources=[Document], position=0)
        menu_facet.bind_links(links=[link_document_content], sources=[Document], position=1)
        menu_facet.bind_links(links=[link_document_properties], sources=[Document], position=2)
        menu_facet.bind_links(links=[link_document_events_view, link_document_version_list], sources=[Document], position=2)

        # Document actions
        menu_object.bind_links(links=[link_document_edit, link_document_document_type_edit, link_document_print, link_document_delete, link_document_download, link_document_clear_transformations, link_document_update_page_count], sources=[Document])

        #register_links([Document], [document_multiple_clear_transformations, document_multiple_delete, document_multiple_download, document_multiple_update_page_count, document_multiple_document_type_edit, link_spacer], menu_name='multi_item_links')

        # Document Version links
        #register_links(DocumentVersion, [document_version_revert, document_version_download])

        # Document page links
        #register_links(DocumentPage, [
        #    document_page_transformation_list, document_page_view,
        #    document_page_text, document_page_edit,
        #])

        # Document page navigation links
        #register_links(DocumentPage, [
        #    document_page_navigation_first, document_page_navigation_previous,
        #    document_page_navigation_next, document_page_navigation_last
        #], menu_name='sidebar')

        #register_links(['documents:document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out, document_page_view_reset], menu_name='form_header')
        #register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
        #register_links('documents:document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
        #register_links('documents:document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
        #register_links(['documents:document_page_transformation_edit', 'documents:document_page_transformation_delete'], [document_page_transformation_create], menu_name='sidebar')

        register_maintenance_links([link_clear_image_cache], namespace='documents', title=_('Documents'))
        register_model_list_columns(Document, [
            {
                'name': _('Thumbnail'), 'attribute':
                encapsulate(lambda x: document_thumbnail(x, gallery_name='documents:document_list', title=getattr(x, 'filename', None), size=THUMBNAIL_SIZE))
            },
            {
                'name': _('Type'), 'attribute': 'document_type'
            }
        ])

        if (not validate_path(document_settings.CACHE_PATH)) or (not document_settings.CACHE_PATH):
            setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())

        menu_setup.bind_links(links=[link_document_type_setup])

        class_permissions(Document, [
            PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD,
            PERMISSION_DOCUMENT_EDIT, PERMISSION_DOCUMENT_NEW_VERSION,
            PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_TRANSFORM,
            PERMISSION_DOCUMENT_VERSION_REVERT, PERMISSION_DOCUMENT_VIEW,
            PERMISSION_EVENTS_VIEW
        ])

        document_search = SearchModel('documents', 'Document', permission=PERMISSION_DOCUMENT_VIEW, serializer_string='documents.serializers.DocumentSerializer')

        # TODO: move these to their respective apps
        # Moving these to other apps cause an ImportError; circular import?
        document_search.add_model_field('document_type__name', label=_('Document type'))
        document_search.add_model_field('versions__mimetype', label=_('MIME type'))
        document_search.add_model_field('label', label=_('Label'))
        document_search.add_model_field('metadata__metadata_type__name', label=_('Metadata type'))
        document_search.add_model_field('metadata__value', label=_('Metadata value'))
        document_search.add_model_field('versions__pages__content', label=_('Content'))
        document_search.add_model_field('description', label=_('Description'))
        document_search.add_model_field('tags__label', label=_('Tags'))

        namespace = StatisticNamespace(name='documents', label=_('Documents'))
        namespace.add_statistic(DocumentStatistics(name='document_stats', label=_('Document tendencies')))
        namespace.add_statistic(DocumentUsageStatistics(name='document_usage', label=_('Document usage')))

        APIEndPoint('documents')

        ModelAttribute(Document, label=_('Label'), name='label', type_name='field')

        FrontPageButton(link=link_document_list_recent)
        FrontPageButton(link=link_document_list)

        registry.register(Document)

        DocumentPage.add_to_class('get_transformation_list', lambda document_page: DocumentPageTransformation.objects.get_for_document_page_as_list(document_page))

        MissingItem(label=_('Create a document type'), description=_('Every uploaded document must be assigned a document type, it is the basic way Mayan EDMS categorizes documents.'), condition=lambda: not DocumentType.objects.exists(), view='documents:document_type_list')
