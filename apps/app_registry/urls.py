from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app_registry.views',
    url(r'^list/$', 'app_list', (), 'app_list'),
)
