from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('metadata.views',
    url(r'^(?P<document_id>\d+)/edit/$', 'metadata_edit', (), 'metadata_edit'),
    url(r'^multiple/edit/$', 'metadata_multiple_edit', (), 'metadata_multiple_edit'),
    url(r'^(?P<document_id>\d+)/add/$', 'metadata_add', (), 'metadata_add'),
    url(r'^multiple/add/$', 'metadata_multiple_add', (), 'metadata_multiple_add'),
    url(r'^(?P<document_id>\d+)/remove/$', 'metadata_remove', (), 'metadata_remove'),
    url(r'^multiple/remove/$', 'metadata_multiple_remove', (), 'metadata_multiple_remove'),
)
