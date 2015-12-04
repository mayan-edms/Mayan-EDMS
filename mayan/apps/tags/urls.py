from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIDocumentTagView, APIDocumentTagListView, APITagDocumentListView,
    APITagListView, APITagView
)
from .views import (
    DocumentTagListView, TagCreateView, TagEditView, TagListView,
    TagTaggedItemListView
)

urlpatterns = patterns(
    'tags.views',
    url(r'^list/$', TagListView.as_view(), name='tag_list'),
    url(r'^create/$', TagCreateView.as_view(), name='tag_create'),
    url(r'^(?P<tag_id>\d+)/delete/$', 'tag_delete', name='tag_delete'),
    url(r'^(?P<pk>\d+)/edit/$', TagEditView.as_view(), name='tag_edit'),
    url(
        r'^(?P<pk>\d+)/documents/$', TagTaggedItemListView.as_view(),
        name='tag_tagged_item_list'
    ),
    url(
        r'^multiple/delete/$', 'tag_multiple_delete',
        name='tag_multiple_delete'
    ),

    url(
        r'^multiple/remove/document/(?P<document_id>\d+)/$',
        'single_document_multiple_tag_remove',
        name='single_document_multiple_tag_remove'
    ),
    url(
        r'^multiple/remove/document/multiple/$',
        'multiple_documents_selection_tag_remove',
        name='multiple_documents_selection_tag_remove'
    ),

    url(
        r'^selection/attach/document/(?P<document_id>\d+)/$', 'tag_attach',
        name='tag_attach'
    ),
    url(
        r'^selection/attach/document/multiple/$', 'tag_multiple_attach',
        name='multiple_documents_tag_attach'
    ),

    url(
        r'^document/(?P<pk>\d+)/tags/$', DocumentTagListView.as_view(),
        name='document_tags'
    ),
)

api_urls = patterns(
    '',
    url(
        r'^tags/(?P<pk>[0-9]+)/documents/$', APITagDocumentListView.as_view(),
        name='tag-document-list'
    ),
    url(r'^tags/(?P<pk>[0-9]+)/$', APITagView.as_view(), name='tag-detail'),
    url(r'^tags/$', APITagListView.as_view(), name='tag-list'),
    url(
        r'^document/(?P<pk>[0-9]+)/tags/$', APIDocumentTagListView.as_view(),
        name='document-tag-list'
    ),
    url(
        r'^document/(?P<document_pk>[0-9]+)/tags/(?P<pk>[0-9]+)/$',
        APIDocumentTagView.as_view(), name='document-tag'
    ),
)
