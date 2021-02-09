from django.conf.urls import url

from .api_views import APICommentListView, APICommentView
from .views import (
    DocumentCommentCreateView, DocumentCommentDeleteView,
    DocumentCommentDetailView, DocumentCommentEditView,
    DocumentCommentListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/comments/$',
        name='comments_for_document', view=DocumentCommentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/comments/add/$',
        name='comment_add', view=DocumentCommentCreateView.as_view()
    ),
    url(
        regex=r'^comments/(?P<comment_id>\d+)/delete/$',
        name='comment_delete', view=DocumentCommentDeleteView.as_view()
    ),
    url(
        regex=r'^comments/(?P<comment_id>\d+)/$', name='comment_details',
        view=DocumentCommentDetailView.as_view()
    ),
    url(
        regex=r'^comments/(?P<comment_id>\d+)/edit/$', name='comment_edit',
        view=DocumentCommentEditView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/comments/$',
        name='comment-list', view=APICommentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$',
        name='comment-detail', view=APICommentView.as_view()
    ),
]
