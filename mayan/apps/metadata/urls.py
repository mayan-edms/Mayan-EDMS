from django.conf.urls import patterns, url

from .api_views import (APIDocumentMetadataListView, APIDocumentMetadataView,
                        APIMetadataTypeListView, APIMetadataTypeView)

urlpatterns = patterns('metadata.views',
    url(r'^(?P<document_id>\d+)/edit/$', 'metadata_edit', (), 'metadata_edit'),
    url(r'^(?P<document_id>\d+)/view/$', 'metadata_view', (), 'metadata_view'),
    url(r'^multiple/edit/$', 'metadata_multiple_edit', (), 'metadata_multiple_edit'),
    url(r'^(?P<document_id>\d+)/add/$', 'metadata_add', (), 'metadata_add'),
    url(r'^multiple/add/$', 'metadata_multiple_add', (), 'metadata_multiple_add'),
    url(r'^(?P<document_id>\d+)/remove/$', 'metadata_remove', (), 'metadata_remove'),
    url(r'^multiple/remove/$', 'metadata_multiple_remove', (), 'metadata_multiple_remove'),

    url(r'^setup/type/list/$', 'setup_metadata_type_list', (), 'setup_metadata_type_list'),
    url(r'^setup/type/create/$', 'setup_metadata_type_create', (), 'setup_metadata_type_create'),
    url(r'^setup/type/(?P<metadatatype_id>\d+)/edit/$', 'setup_metadata_type_edit', (), 'setup_metadata_type_edit'),
    url(r'^setup/type/(?P<metadatatype_id>\d+)/delete/$', 'setup_metadata_type_delete', (), 'setup_metadata_type_delete'),

    url(r'^setup/document/type/(?P<document_type_id>\d+)/metadata/default/edit/$', 'setup_document_type_metadata', (), 'setup_document_type_metadata'),
)

api_urls = patterns('',
    url(r'^metadatatypes/$', APIMetadataTypeListView.as_view(), name='metadatatype-list'),
    url(r'^metadatatypes/(?P<pk>[0-9]+)/$', APIMetadataTypeView.as_view(), name='metadatatype-detail'),
    url(r'^document/(?P<pk>[0-9]+)/metadata/$', APIDocumentMetadataListView.as_view(), name='documentmetadata-list'),
    url(r'^document/(?P<document_pk>[0-9]+)/metadata/(?P<pk>[0-9]+)/$', APIDocumentMetadataView.as_view(), name='documentmetadata-detail'),
)
