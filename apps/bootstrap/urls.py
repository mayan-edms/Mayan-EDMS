from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bootstrap.views',
    url(r'^type/list/$', 'bootstrap_type_list', (), 'bootstrap_type_list'),
    url(r'^(?P<bootstrap_setup_pk>\d+)/execute/$', 'bootstrap_execute', (), 'bootstrap_execute'),
    url(r'^nuke/$', 'erase_database_view', (), 'erase_database_view'),
)
