from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('folders.views',
    url(r'^list/$', 'folder_list', (), 'folder_list'),
    url(r'^create/$', 'folder_create', (), 'folder_create'),
    url(r'^(?P<folder_id>\d+)/edit/$', 'folder_edit', (), 'folder_edit'),
    url(r'^(?P<folder_id>\d+)/delete/$', 'folder_delete', (), 'folder_delete'),
    url(r'^(?P<folder_id>\d+)/$', 'folder_view', (), 'folder_view'),
)
