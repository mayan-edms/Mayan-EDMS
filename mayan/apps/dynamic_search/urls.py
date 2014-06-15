from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dynamic_search.views',
    url(r'^$', 'search', (), 'search'),
    url(r'^advanced/$', 'search', {'advanced': True}, 'search_advanced'),
    url(r'^again/$', 'search_again', (), 'search_again'),
    url(r'^results/$', 'results', (), 'results'),
)
