from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import CommentCreateView, DocumentCommentListView

urlpatterns = patterns(
    'document_comments.views',
    url(
        r'^comment/(?P<comment_id>\d+)/delete/$', 'comment_delete',
        name='comment_delete'
    ),
    url(
        r'^comment/multiple/delete/$', 'comment_multiple_delete',
        name='comment_multiple_delete'
    ),
    url(
        r'^(?P<pk>\d+)/comment/add/$', CommentCreateView.as_view(),
        name='comment_add'
    ),
    url(
        r'^(?P<pk>\d+)/comment/list/$',
        DocumentCommentListView.as_view(), name='comments_for_document'
    ),
)
