from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentTagView, APIDocumentTagListView, APITagDocumentListView,
    APITagListView, APITagView
)
from .views import (
    DocumentTagListView, TagAttachActionView, TagCreateView,
    TagDeleteActionView, TagEditView, TagListView, TagRemoveActionView,
    TagDocumentListView
)

urlpatterns = [
    url(regex=r'^tags/$', view=TagListView.as_view(), name='tag_list'),
    url(regex=r'^tags/create/$', view=TagCreateView.as_view(), name='tag_create'),
    url(
        regex=r'^tags/(?P<pk>\d+)/delete/$', view=TagDeleteActionView.as_view(),
        name='tag_delete'
    ),
    url(
        regex=r'^tags/(?P<pk>\d+)/edit/$', view=TagEditView.as_view(),
        name='tag_edit'
    ),
    url(
        regex=r'^tags/(?P<pk>\d+)/documents/$', view=TagDocumentListView.as_view(),
        name='tag_document_list'
    ),
    url(
        regex=r'^tags/multiple/delete/$', view=TagDeleteActionView.as_view(),
        name='tag_multiple_delete'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/tags/remove/$',
        view=TagRemoveActionView.as_view(),
        name='single_document_multiple_tag_remove'
    ),
    url(
        regex=r'^documents/multiple/tags/remove/$',
        view=TagRemoveActionView.as_view(),
        name='multiple_documents_selection_tag_remove'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/tags/attach/$',
        view=TagAttachActionView.as_view(), name='tag_attach'
    ),
    url(
        regex=r'^documents/multiple/tags/attach/$',
        view=TagAttachActionView.as_view(), name='multiple_documents_tag_attach'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/tags/$',
        view=DocumentTagListView.as_view(), name='document_tag_list'
    ),
]

api_urls = [
    url(regex=r'^tags/$', view=APITagListView.as_view(), name='tag-list'),
    url(
        regex=r'^tags/(?P<pk>[0-9]+)/$', view=APITagView.as_view(),
        name='tag-detail'
    ),
    url(
        regex=r'^tags/(?P<pk>[0-9]+)/documents/$',
        view=APITagDocumentListView.as_view(), name='tag-document-list'
    ),
    url(
        regex=r'^documents/(?P<document_pk>[0-9]+)/tags/$',
        view=APIDocumentTagListView.as_view(), name='document-tag-list'
    ),
    url(
        regex=r'^documents/(?P<document_pk>[0-9]+)/tags/(?P<pk>[0-9]+)/$',
        view=APIDocumentTagView.as_view(), name='document-tag-detail'
    ),
]
