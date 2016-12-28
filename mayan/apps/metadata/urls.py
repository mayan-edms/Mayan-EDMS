from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentMetadataListView, APIDocumentMetadataView,
    APIDocumentTypeMetadataTypeOptionalListView,
    APIDocumentTypeMetadataTypeRequiredListView,
    APIDocumentTypeMetadataTypeView, APIMetadataTypeListView,
    APIMetadataTypeView
)
from .views import (
    DocumentMetadataAddView, DocumentMetadataEditView,
    DocumentMetadataListView, DocumentMetadataRemoveView,
    MetadataTypeCreateView, MetadataTypeDeleteView, MetadataTypeEditView,
    MetadataTypeListView, SetupDocumentTypeMetadataOptionalView,
    SetupDocumentTypeMetadataRequiredView
)

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/edit/$', DocumentMetadataEditView.as_view(),
        name='metadata_edit'
    ),
    url(
        r'^multiple/edit/$', DocumentMetadataEditView.as_view(),
        name='metadata_multiple_edit'
    ),
    url(
        r'^(?P<pk>\d+)/view/$', DocumentMetadataListView.as_view(),
        name='metadata_view'
    ),
    url(
        r'^(?P<pk>\d+)/add/$', DocumentMetadataAddView.as_view(),
        name='metadata_add'
    ),
    url(
        r'^multiple/add/$', DocumentMetadataAddView.as_view(),
        name='metadata_multiple_add'
    ),
    url(
        r'^(?P<pk>\d+)/remove/$', DocumentMetadataRemoveView.as_view(),
        name='metadata_remove'
    ),
    url(
        r'^multiple/remove/$', DocumentMetadataRemoveView.as_view(),
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
]

api_urls = [
    url(
        r'^metadata_types/$', APIMetadataTypeListView.as_view(),
        name='metadatatype-list'
    ),
    url(
        r'^metadata_types/(?P<pk>[0-9]+)/$', APIMetadataTypeView.as_view(),
        name='metadatatype-detail'
    ),
    url(
        r'^document/metadata/(?P<pk>[0-9]+)/$',
        APIDocumentMetadataView.as_view(), name='documentmetadata-detail'
    ),
    url(
        r'^document/(?P<pk>\d+)/metadata/$',
        APIDocumentMetadataListView.as_view(), name='documentmetadata-list'
    ),
    url(
        r'^document_type/(?P<document_type_pk>[0-9]+)/metadata_types/optional/$',
        APIDocumentTypeMetadataTypeOptionalListView.as_view(),
        name='documenttypeoptionalmetadatatype-list'
    ),
    url(
        r'^document_type/(?P<document_type_pk>[0-9]+)/metadata_types/required/$',
        APIDocumentTypeMetadataTypeRequiredListView.as_view(),
        name='documenttyperequiredmetadatatype-list'
    ),
    url(
        r'^document_type_metadata_type/(?P<pk>\d+)/$',
        APIDocumentTypeMetadataTypeView.as_view(),
        name='documenttypemetadatatype-detail'
    ),
]
