from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    DocumentCommentCreateView, DocumentCommentDeleteView,
    DocumentCommentListView
)

urlpatterns = [
    url(
        r'^comment/(?P<pk>\d+)/delete/$', DocumentCommentDeleteView.as_view(),
        name='comment_delete'
    ),
    url(
        r'^(?P<pk>\d+)/comment/add/$', DocumentCommentCreateView.as_view(),
        name='comment_add'
    ),
    url(
        r'^(?P<pk>\d+)/comment/list/$',
        DocumentCommentListView.as_view(), name='comments_for_document'
    ),
]
