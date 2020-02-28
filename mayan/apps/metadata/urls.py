from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    DocumentMetadataAPIViewSet, DocumentTypeMetadataTypeRelationAPIViewSet,
    MetadataTypeAPIViewSet, MetadataTypeDocumentTypeRelationAPIViewSet
)
from .views import (
    DocumentMetadataAddView, DocumentMetadataEditView,
    DocumentMetadataListView, DocumentMetadataRemoveView,
    MetadataTypeCreateView, MetadataTypeDeleteView, MetadataTypeEditView,
    MetadataTypeListView, SetupDocumentTypeMetadataTypes,
    SetupMetadataTypesDocumentTypes
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/add/$',
        name='metadata_add', view=DocumentMetadataAddView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/medata/edit/$',
        name='metadata_edit', view=DocumentMetadataEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/remove/$',
        name='metadata_remove', view=DocumentMetadataRemoveView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/view/$',
        name='metadata_view', view=DocumentMetadataListView.as_view()
    ),
    url(
        regex=r'^documents/multiple/metadata/edit/$',
        name='metadata_multiple_edit', view=DocumentMetadataEditView.as_view()
    ),
    url(
        regex=r'^documents/multiple/add/$', name='metadata_multiple_add',
        view=DocumentMetadataAddView.as_view()
    ),
    url(
        regex=r'^documents/multiple/remove/$',
        name='metadata_multiple_remove',
        view=DocumentMetadataRemoveView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/metadata_types/$',
        name='setup_document_type_metadata_types',
        view=SetupDocumentTypeMetadataTypes.as_view()
    ),
    url(
        regex=r'^metadata_types/$', name='setup_metadata_type_list',
        view=MetadataTypeListView.as_view()
    ),
    url(
        regex=r'^metadata_types/create/$', name='setup_metadata_type_create',
        view=MetadataTypeCreateView.as_view()
    ),
    url(
        regex=r'^metadata_types/(?P<metadata_type_id>\d+)/delete/$',
        name='setup_metadata_type_delete',
        view=MetadataTypeDeleteView.as_view()
    ),
    url(
        regex=r'^metadata_types/(?P<metadata_type_id>\d+)/document_types/$',
        name='setup_metadata_type_document_types',
        view=SetupMetadataTypesDocumentTypes.as_view()
    ),
    url(
        regex=r'^metadata_types/(?P<metadata_type_id>\d+)/edit/$',
        name='setup_metadata_type_edit', view=MetadataTypeEditView.as_view()
    ),
]

api_router_entries = (
    {
        'prefix': r'document_types/(?P<document_type_id>[^/.]+)/metadata_type_relations',
        'viewset': DocumentTypeMetadataTypeRelationAPIViewSet,
        'basename': 'document_type-metadata_type_relation'
    },
    {
        'prefix': r'documents/(?P<document_id>[^/.]+)/metadata',
        'viewset': DocumentMetadataAPIViewSet, 'basename': 'document_metadata'
    },
    {
        'prefix': r'metadata_types', 'viewset': MetadataTypeAPIViewSet,
        'basename': 'metadata_type'
    },
    {
        'prefix': r'metadata_types/(?P<metadata_type_id>[^/.]+)/document_type_relations',
        'viewset': MetadataTypeDocumentTypeRelationAPIViewSet,
        'basename': 'metadata_type-document_type_relation'
    },
)
