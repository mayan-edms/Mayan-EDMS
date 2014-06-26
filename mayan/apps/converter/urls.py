from django.conf.urls import patterns, url

urlpatterns = patterns('converter.views',
    url(r'^formats/$', 'formats_list', (), 'formats_list'),
)
