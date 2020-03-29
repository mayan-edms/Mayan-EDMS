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
        regex=r'^document_types/(?P<document_type_id>\d+)/metadata_types/$',
        name='setup_document_type_metadata_types',
        view=SetupDocumentTypeMetadataTypes.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/edit/$',
        name='metadata_edit', view=DocumentMetadataEditView.as_view()
    ),
    url(
        regex=r'^documents/multiple/metadata/edit/$',
        name='metadata_multiple_edit', view=DocumentMetadataEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/view/$',
        name='metadata_view', view=DocumentMetadataListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/add/$',
        name='metadata_add', view=DocumentMetadataAddView.as_view()
    ),
    url(
        regex=r'^documents/multiple/metadata/add/$',
        name='metadata_multiple_add', view=DocumentMetadataAddView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/metadata/remove/$',
        name='metadata_remove', view=DocumentMetadataRemoveView.as_view()
    ),
    url(
        regex=r'^documents/multiple/metadata/remove/$',
        name='metadata_multiple_remove',
        view=DocumentMetadataRemoveView.as_view()
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
        regex=r'^metadata_types/(?P<metadata_type_id>\d+)/edit/$',
        name='setup_metadata_type_edit', view=MetadataTypeEditView.as_view()
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
    )
]

api_urls = [
    url(
        regex=r'^metadata_types/$', name='metadatatype-list',
        view=APIMetadataTypeListView.as_view()
    ),
    url(
        regex=r'^metadata_types/(?P<metadata_type_pk>\d+)/$',
        name='metadatatype-detail', view=APIMetadataTypeView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_pk>\d+)/metadata_types/$',
        name='documenttypemetadatatype-list',
        view=APIDocumentTypeMetadataTypeListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_pk>\d+)/metadata_types/(?P<metadata_type_pk>\d+)/$',
        name='documenttypemetadatatype-detail',
        view=APIDocumentTypeMetadataTypeView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/metadata/$',
        name='documentmetadata-list',
        view=APIDocumentMetadataListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/metadata/(?P<metadata_pk>\d+)/$',
        name='documentmetadata-detail',
        view=APIDocumentMetadataView.as_view()
    )
]
