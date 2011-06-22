from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dynamic_search.views',
    url(r'^search/$', 'search', (), 'search'),
    url(r'^search/advanced/$', 'search', { 'advanced': True }, 'search_advanced'),
    url(r'^results/$', 'results', (), 'results'),
)
