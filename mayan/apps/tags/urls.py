from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import DocumentTagAPIViewSet, TagAPIViewSet


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
        name='document_tag_multiple_attach', view=TagAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/tags/multiple/remove/$',
        name='document_tag_multiple_remove',
        view=TagRemoveActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/tags/multiple/attach/$',
        name='documents_multiple_tag_multiple_attach',
        view=TagAttachActionView.as_view()
    ),
    url(
        regex=r'^documents/multiple/tags/multiple/remove/$',
        name='documents_multiple_tag_multiple_remove',
        view=TagRemoveActionView.as_view()
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

api_router_entries = (
    {
        'prefix': r'tags', 'viewset': TagAPIViewSet, 'basename': 'tag'
    },
    {
        'prefix': r'documents', 'viewset': DocumentTagAPIViewSet,
        'basename': 'document'
    }
)
