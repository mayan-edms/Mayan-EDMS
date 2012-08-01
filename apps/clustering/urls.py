from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('clustering.views',
    url(r'^node/list/$', 'node_list', (), 'node_list'),
    url(r'^edit/$', 'clustering_config_edit', (), 'clustering_config_edit'),
)
