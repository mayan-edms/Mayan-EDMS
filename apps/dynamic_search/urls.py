from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dynamic_search.views',
    url(r'^search/$', 'search', (), 'search'),
    url(r'^results/$', 'results', (), 'results'),
)
