from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('document_comments.views',
    url(r'^comment/(?P<comment_id>\d+)/delete/$', 'comment_delete', (), 'comment_delete'),
    url(r'^comment/multiple/delete/$', 'comment_multiple_delete', (), 'comment_multiple_delete'),
    url(r'^(?P<document_id>\d+)/comment/add/$', 'comment_add', (), 'comment_add'),
    url(r'^(?P<document_id>\d+)/comment/list/$', 'comments_for_document', (), 'comments_for_document'),
)
