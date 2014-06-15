from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bootstrap.views',
    url(r'^setup/list/$', 'bootstrap_setup_list', (), 'bootstrap_setup_list'),
    url(r'^setup/create/$', 'bootstrap_setup_create', (), 'bootstrap_setup_create'),
    url(r'^setup/(?P<bootstrap_setup_pk>\d+)/edit/$', 'bootstrap_setup_edit', (), 'bootstrap_setup_edit'),
    url(r'^setup/(?P<bootstrap_setup_pk>\d+)/delete/$', 'bootstrap_setup_delete', (), 'bootstrap_setup_delete'),
    url(r'^setup/(?P<bootstrap_setup_pk>\d+)/$', 'bootstrap_setup_view', (), 'bootstrap_setup_view'),
    url(r'^setup/(?P<bootstrap_setup_pk>\d+)/execute/$', 'bootstrap_setup_execute', (), 'bootstrap_setup_execute'),
    url(r'^setup/(?P<bootstrap_setup_pk>\d+)/export/$', 'bootstrap_setup_export', (), 'bootstrap_setup_export'),
    url(r'^setup/dump/$', 'bootstrap_setup_dump', (), 'bootstrap_setup_dump'),
    url(r'^setup/import/file/$', 'bootstrap_setup_import_from_file', (), 'bootstrap_setup_import_from_file'),
    url(r'^setup/import/url/$', 'bootstrap_setup_import_from_url', (), 'bootstrap_setup_import_from_url'),
    url(r'^setup/repository/sync/$', 'bootstrap_setup_repository_sync', (), 'bootstrap_setup_repository_sync'),
    url(r'^nuke/$', 'erase_database_view', (), 'erase_database_view'),
)
