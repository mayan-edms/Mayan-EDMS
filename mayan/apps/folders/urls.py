from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIDocumentFolderListView, APIFolderDocumentListView,
    APIFolderDocumentView, APIFolderListView, APIFolderView
)
from .views import FolderDetailView, FolderListView

urlpatterns = patterns('folders.views',
    url(r'^list/$', FolderListView.as_view(), name='folder_list'),
    url(r'^create/$', 'folder_create', (), 'folder_create'),
    url(r'^(?P<folder_id>\d+)/edit/$', 'folder_edit', (), 'folder_edit'),
    url(r'^(?P<folder_id>\d+)/delete/$', 'folder_delete', (), 'folder_delete'),
    url(r'^(?P<pk>\d+)/$', FolderDetailView.as_view(), name='folder_view'),
    url(r'^(?P<folder_id>\d+)/remove/document/multiple/$', 'folder_document_multiple_remove', (), 'folder_document_multiple_remove'),

    url(r'^document/(?P<document_id>\d+)/folder/add/$', 'folder_add_document', (), 'folder_add_document'),
    url(r'^document/multiple/folder/add/$', 'folder_add_multiple_documents', (), 'folder_add_multiple_documents'),
    url(r'^document/(?P<document_id>\d+)/folder/list/$', 'document_folder_list', (), 'document_folder_list'),

    url(r'^(?P<folder_pk>\d+)/acl/list/$', 'folder_acl_list', (), 'folder_acl_list'),
)

api_urls = patterns('',
    url(r'^folders/(?P<pk>[0-9]+)/documents/(?P<document_pk>[0-9]+)/$', APIFolderDocumentView.as_view(), name='folder-document'),
    url(r'^folders/(?P<pk>[0-9]+)/documents/$', APIFolderDocumentListView.as_view(), name='folder-document-list'),
    url(r'^folders/(?P<pk>[0-9]+)/$', APIFolderView.as_view(), name='folder-detail'),
    url(r'^folders/$', APIFolderListView.as_view(), name='folder-list'),
    url(r'^document/(?P<pk>[0-9]+)/folders/$', APIDocumentFolderListView.as_view(), name='document-folder-list'),
)
