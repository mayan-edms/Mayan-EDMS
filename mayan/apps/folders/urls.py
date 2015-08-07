from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIDocumentFolderListView, APIFolderDocumentListView,
    APIFolderDocumentView, APIFolderListView, APIFolderView
)
from .views import (
    DocumentFolderListView, FolderCreateView, FolderDetailView, FolderEditView,
    FolderListView
)

urlpatterns = patterns(
    'folders.views',
    url(r'^list/$', FolderListView.as_view(), name='folder_list'),
    url(r'^create/$', FolderCreateView.as_view(), name='folder_create'),
    url(r'^(?P<pk>\d+)/edit/$', FolderEditView.as_view(), name='folder_edit'),
    url(
        r'^(?P<folder_id>\d+)/delete/$', 'folder_delete', name='folder_delete'
    ),
    url(r'^(?P<pk>\d+)/$', FolderDetailView.as_view(), name='folder_view'),
    url(
        r'^(?P<folder_id>\d+)/remove/document/multiple/$',
        'folder_document_multiple_remove',
        name='folder_document_multiple_remove'
    ),

    url(
        r'^document/(?P<document_id>\d+)/folder/add/$',
        'folder_add_document', name='folder_add_document'
    ),
    url(
        r'^document/multiple/folder/add/$', 'folder_add_multiple_documents',
        name='folder_add_multiple_documents'
    ),
    url(
        r'^document/(?P<pk>\d+)/folder/list/$',
        DocumentFolderListView.as_view(), name='document_folder_list'
    ),
)

api_urls = patterns(
    '',
    url(
        r'^folders/(?P<folder_pk>[0-9]+)/documents/(?P<pk>[0-9]+)/$',
        APIFolderDocumentView.as_view(), name='folder-document'
    ),
    url(
        r'^folders/(?P<pk>[0-9]+)/documents/$',
        APIFolderDocumentListView.as_view(), name='folder-document-list'
    ),
    url(
        r'^folders/(?P<pk>[0-9]+)/$', APIFolderView.as_view(),
        name='folder-detail'
    ),
    url(r'^folders/$', APIFolderListView.as_view(), name='folder-list'),
    url(
        r'^document/(?P<pk>[0-9]+)/folders/$',
        APIDocumentFolderListView.as_view(), name='document-folder-list'
    ),
)
