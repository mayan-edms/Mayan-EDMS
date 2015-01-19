from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIDocumentTagView, APIDocumentTagListView, APITagDocumentListView,
    APITagListView, APITagView
)
from .views import TagTaggedItemListView

urlpatterns = patterns('tags.views',
    url(r'^list/$', 'tag_list', (), 'tag_list'),
    url(r'^create/$', 'tag_create', (), 'tag_create'),
    url(r'^(?P<tag_id>\d+)/delete/$', 'tag_delete', (), 'tag_delete'),
    url(r'^(?P<tag_id>\d+)/edit/$', 'tag_edit', (), 'tag_edit'),
    url(r'^(?P<pk>\d+)/documents/$', TagTaggedItemListView.as_view(), name='tag_tagged_item_list'),
    url(r'^multiple/delete/$', 'tag_multiple_delete', (), 'tag_multiple_delete'),

    url(r'^multiple/remove/document/(?P<document_id>\d+)/$', 'single_document_multiple_tag_remove', (), 'single_document_multiple_tag_remove'),
    url(r'^multiple/remove/document/multiple/$', 'multiple_documents_selection_tag_remove', (), 'multiple_documents_selection_tag_remove'),

    url(r'^selection/attach/document/(?P<document_id>\d+)/$', 'tag_attach', (), 'tag_attach'),
    url(r'^selection/attach/document/multiple/$', 'tag_multiple_attach', (), 'tag_multiple_attach'),

    url(r'^for/document/(?P<document_id>\d+)/$', 'document_tags', (), 'document_tags'),

    url(r'^(?P<tag_pk>\d+)/acl/list/$', 'tag_acl_list', (), 'tag_acl_list'),
)

api_urls = patterns('',
    url(r'^tags/(?P<pk>[0-9]+)/documents/$', APITagDocumentListView.as_view(), name='tag-document-list'),
    url(r'^tags/(?P<pk>[0-9]+)/$', APITagView.as_view(), name='tag-detail'),
    url(r'^tags/$', APITagListView.as_view(), name='tag-list'),
    url(r'^document/(?P<pk>[0-9]+)/tags/$', APIDocumentTagListView.as_view(), name='document-tag-list'),
    url(r'^document/(?P<document_pk>[0-9]+)/tags/(?P<pk>[0-9]+)/$', APIDocumentTagView.as_view(), name='document-tag'),
)
