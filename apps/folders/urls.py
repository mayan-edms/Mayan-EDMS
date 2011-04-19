from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('folders.views',
    url(r'^list/$', 'folder_list', (), 'folder_list'),
    url(r'^create/$', 'folder_create', (), 'folder_create'),
    url(r'^(?P<folder_id>\d+)/edit/$', 'folder_edit', (), 'folder_edit'),
    url(r'^(?P<folder_id>\d+)/delete/$', 'folder_delete', (), 'folder_delete'),
    url(r'^(?P<folder_id>\d+)/$', 'folder_view', (), 'folder_view'),
    url(r'^document/multiple/remove/$', 'folder_document_multiple_remove', (), 'folder_document_multiple_remove'),

    url(r'^add_document/(?P<document_id>\d+)/$', 'folder_add_document', (), 'folder_add_document'),
)
