from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('statistics.views',
    url(r'^$', 'statistics_view', (), 'statistics'),
)
