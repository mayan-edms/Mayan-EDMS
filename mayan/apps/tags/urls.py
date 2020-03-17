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
    url(
        regex=r'^documents/(?P<document_id>\d+)/tags/$',
        name='document_tag_list', view=DocumentTagListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/attach/$',
        name='tag_attach', view=TagAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/remove/$',
        name='single_document_multiple_tag_remove',
        view=TagRemoveActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/tags/multiple/remove/$',
        name='multiple_documents_selection_tag_remove',
        view=TagRemoveActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/tags/multiple/attach/$',
        name='multiple_documents_tag_attach',
        view=TagAttachActionView.as_view()
    ),
    url(regex=r'^tags/$', name='tag_list', view=TagListView.as_view()),
    url(
        regex=r'^tags/create/$', name='tag_create',
        view=TagCreateView.as_view()
    ),
    url(
        regex=r'^tags/(?P<tag_id>\d+)/delete/$', name='tag_delete',
        view=TagDeleteActionView.as_view()
    ),
    url(
        regex=r'^tags/(?P<tag_id>\d+)/edit/$', name='tag_edit',
        view=TagEditView.as_view()
    ),
    url(
        regex=r'^tags/(?P<tag_id>\d+)/documents/$', name='tag_document_list',
        view=TagDocumentListView.as_view()
    ),
    url(
        regex=r'^tags/multiple/delete/$', name='tag_multiple_delete',
        view=TagDeleteActionView.as_view()
    )
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
