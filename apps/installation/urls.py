from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('installation.views',
    url(r'^$', 'namespace_list', (), 'namespace_list'),
    url(r'^(?P<namespace_id>\w+)/details/$', 'namespace_details', (), 'namespace_details'),
)
