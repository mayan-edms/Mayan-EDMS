from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('folders.views',
    url(r'^list/$', 'folder_list', (), 'folder_list'),
    url(r'^create/$', 'folder_create', (), 'folder_create'),
    url(r'^(?P<folder_id>\d+)/edit/$', 'folder_edit', (), 'folder_edit'),
    url(r'^(?P<folder_id>\d+)/delete/$', 'folder_delete', (), 'folder_delete'),
    url(r'^(?P<folder_id>\d+)/$', 'folder_view', (), 'folder_view'),
    url(r'^(?P<folder_id>\d+)/remove/document/multiple/$', 'folder_document_multiple_remove', (), 'folder_document_multiple_remove'),

    url(r'^document/(?P<document_id>\d+)/folder/add/$', 'folder_add_document', (), 'folder_add_document'),
    url(r'^document/multiple/folder/add/$', 'folder_add_multiple_documents', (), 'folder_add_multiple_documents'),
    url(r'^document/(?P<document_id>\d+)/folder/list/$', 'document_folder_list', (), 'document_folder_list'),

    url(r'^(?P<folder_pk>\d+)/acl/list/$', 'folder_acl_list', (), 'folder_acl_list'),
)
