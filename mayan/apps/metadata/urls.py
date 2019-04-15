from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentMetadataListView, APIDocumentMetadataView,
    APIDocumentTypeMetadataTypeListView, APIDocumentTypeMetadataTypeView,
    APIMetadataTypeListView, APIMetadataTypeView
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
        regex=r'^(?P<pk>\d+)/edit/$', view=DocumentMetadataEditView.as_view(),
        name='metadata_edit'
    ),
    url(
        regex=r'^multiple/edit/$', view=DocumentMetadataEditView.as_view(),
        name='metadata_multiple_edit'
    ),
    url(
        regex=r'^(?P<pk>\d+)/view/$', view=DocumentMetadataListView.as_view(),
        name='metadata_view'
    ),
    url(
        regex=r'^(?P<pk>\d+)/add/$', view=DocumentMetadataAddView.as_view(),
        name='metadata_add'
    ),
    url(
        regex=r'^multiple/add/$', view=DocumentMetadataAddView.as_view(),
        name='metadata_multiple_add'
    ),
    url(
        regex=r'^(?P<pk>\d+)/remove/$',
        view=DocumentMetadataRemoveView.as_view(), name='metadata_remove'
    ),
    url(
        regex=r'^multiple/remove/$', view=DocumentMetadataRemoveView.as_view(),
        name='metadata_multiple_remove'
    ),
    url(
        regex=r'^setup/type/list/$', view=MetadataTypeListView.as_view(),
        name='setup_metadata_type_list'
    ),
    url(
        regex=r'^setup/type/create/$', view=MetadataTypeCreateView.as_view(),
        name='setup_metadata_type_create'
    ),
    url(
        regex=r'^setup/type/(?P<pk>\d+)/edit/$',
        view=MetadataTypeEditView.as_view(), name='setup_metadata_type_edit'
    ),
    url(
        regex=r'^setup/type/(?P<pk>\d+)/delete/$',
        view=MetadataTypeDeleteView.as_view(), name='setup_metadata_type_delete'
    ),
    url(
        regex=r'^setup/document_types/(?P<pk>\d+)/metadata_types/$',
        view=SetupDocumentTypeMetadataTypes.as_view(),
        name='setup_document_type_metadata_types'
    ),
    url(
        regex=r'^setup/metadata_types/(?P<pk>\d+)/document_types/$',
        view=SetupMetadataTypesDocumentTypes.as_view(),
        name='setup_metadata_type_document_types'
    ),
]

api_urls = [
    url(
        regex=r'^metadata_types/$', view=APIMetadataTypeListView.as_view(),
        name='metadatatype-list'
    ),
    url(
        regex=r'^metadata_types/(?P<metadata_type_pk>\d+)/$',
        view=APIMetadataTypeView.as_view(), name='metadatatype-detail'
    ),
    url(
        regex=r'^document_types/(?P<document_type_pk>\d+)/metadata_types/$',
        view=APIDocumentTypeMetadataTypeListView.as_view(),
        name='documenttypemetadatatype-list'
    ),
    url(
        regex=r'^document_types/(?P<document_type_pk>\d+)/metadata_types/(?P<metadata_type_pk>\d+)/$',
        view=APIDocumentTypeMetadataTypeView.as_view(),
        name='documenttypemetadatatype-detail'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/metadata/$',
        view=APIDocumentMetadataListView.as_view(), name='documentmetadata-list'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/metadata/(?P<metadata_pk>\d+)/$',
        view=APIDocumentMetadataView.as_view(), name='documentmetadata-detail'
    ),
]
