from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bootstrap.views',
    url(r'^type/list/$', 'bootstrap_type_list', (), 'bootstrap_type_list'),
    url(r'^(?P<bootstrap_name>\w+)/execute/$', 'bootstrap_execute', (), 'bootstrap_execute'),
)
