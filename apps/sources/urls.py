from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('sources.views',
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),

    url(r'^upload/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/$', 'upload_interactive', (), 'upload_interactive'),
    url(r'^upload/interactive/$', 'upload_interactive', (), 'upload_interactive'),
)
