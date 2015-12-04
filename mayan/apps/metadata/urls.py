from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIDocumentMetadataListView, APIDocumentMetadataView,
    APIDocumentTypeMetadataTypeOptionalListView,
    APIDocumentTypeMetadataTypeRequiredListView,
    APIDocumentTypeMetadataTypeRequiredView, APIMetadataTypeListView,
    APIMetadataTypeView
)
from .views import (
    DocumentMetadataListView, MetadataTypeCreateView, MetadataTypeDeleteView,
    MetadataTypeEditView, MetadataTypeListView,
    SetupDocumentTypeMetadataOptionalView,
    SetupDocumentTypeMetadataRequiredView
)

urlpatterns = patterns(
    'metadata.views',
    url(
        r'^(?P<document_id>\d+)/edit/$', 'metadata_edit', name='metadata_edit'
    ),
    url(
        r'^(?P<pk>\d+)/view/$', DocumentMetadataListView.as_view(),
        name='metadata_view'
    ),
    url(
        r'^multiple/edit/$', 'metadata_multiple_edit',
        name='metadata_multiple_edit'
    ),
    url(r'^(?P<document_id>\d+)/add/$', 'metadata_add', name='metadata_add'),
    url(
        r'^multiple/add/$', 'metadata_multiple_add',
        name='metadata_multiple_add'
    ),
    url(
        r'^(?P<document_id>\d+)/remove/$', 'metadata_remove',
        name='metadata_remove'
    ),
    url(
        r'^multiple/remove/$', 'metadata_multiple_remove',
        name='metadata_multiple_remove'
    ),

    url(
        r'^setup/type/list/$', MetadataTypeListView.as_view(),
        name='setup_metadata_type_list'
    ),
    url(
        r'^setup/type/create/$', MetadataTypeCreateView.as_view(),
        name='setup_metadata_type_create'
    ),
    url(
        r'^setup/type/(?P<pk>\d+)/edit/$', MetadataTypeEditView.as_view(),
        name='setup_metadata_type_edit'
    ),
    url(
        r'^setup/type/(?P<pk>\d+)/delete/$',
        MetadataTypeDeleteView.as_view(), name='setup_metadata_type_delete'
    ),

    url(
        r'^setup/document/type/(?P<pk>\d+)/metadata/edit/$',
        SetupDocumentTypeMetadataOptionalView.as_view(),
        name='setup_document_type_metadata'
    ),
    url(
        r'^setup/document/type/(?P<pk>\d+)/metadata/edit/required/$',
        SetupDocumentTypeMetadataRequiredView.as_view(),
        name='setup_document_type_metadata_required'
    ),
)

api_urls = patterns(
    '',
    url(
        r'^metadatatypes/$', APIMetadataTypeListView.as_view(),
        name='metadatatype-list'
    ),
    url(
        r'^metadatatypes/(?P<pk>[0-9]+)/$', APIMetadataTypeView.as_view(),
        name='metadatatype-detail'
    ),
    url(
        r'^document/metadata/(?P<pk>[0-9]+)/$',
        APIDocumentMetadataView.as_view(), name='documentmetadata-detail'
    ),
    url(
        r'^document/(?P<document_pk>[0-9]+)/metadata/$',
        APIDocumentMetadataListView.as_view(), name='documentmetadata-list'
    ),
    url(
        r'^document_type/(?P<document_type_pk>[0-9]+)/metadatatypes/optional/$',
        APIDocumentTypeMetadataTypeOptionalListView.as_view(),
        name='documenttypemetadatatype-list'
    ),
    url(
        r'^document_type/(?P<document_type_pk>[0-9]+)/metadatatypes/required/$',
        APIDocumentTypeMetadataTypeRequiredListView.as_view(),
        name='documenttypemetadatatype-list'
    ),
    url(
        r'^document_type/(?P<document_type_pk>[0-9]+)/metadatatypes/(?P<metadata_type_pk>[0-9]+)/$',
        APIDocumentTypeMetadataTypeRequiredView.as_view(),
        name='documenttypemetadatatype-detail'
    ),
)
