from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('document_indexing.views',
    url(r'^(?P<index_id>\d+)/list/$', 'index_instance_list', (), 'index_instance_list'),
    url(r'^list/$', 'index_instance_list', (), 'index_instance_list'),
    url(r'^rebuild/all/$', 'rebuild_index_instances', (), 'rebuild_index_instances'),
)
