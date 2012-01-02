from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tags.views',
    url(r'^list/$', 'tag_list', (), 'tag_list'),
    url(r'^create/$', 'tag_create', (), 'tag_create'),
    url(r'^(?P<tag_id>\d+)/delete/$', 'tag_delete', (), 'tag_delete'),
    url(r'^(?P<tag_id>\d+)/edit/$', 'tag_edit', (), 'tag_edit'),
    url(r'^(?P<tag_id>\d+)/tagged_item/list/$', 'tag_tagged_item_list', (), 'tag_tagged_item_list'),
    url(r'^multiple/delete/$', 'tag_multiple_delete', (), 'tag_multiple_delete'),

    url(r'^(?P<tag_id>\d+)/remove_from_document/(?P<document_id>\d+)/$', 'tag_remove', (), 'tag_remove'),
    url(r'^multiple/remove_from_document/(?P<document_id>\d+)/$', 'tag_multiple_remove', (), 'tag_multiple_remove'),
    url(r'^document/(?P<document_id>\d+)/add/$', 'tag_attach', (), 'tag_attach'),
    url(r'^document/(?P<document_id>\d+)/list/$', 'document_tags', (), 'document_tags'),
    
    url(r'^(?P<tag_pk>\d+)/acl/list/$', 'tag_acl_list', (), 'tag_acl_list'),
    url(r'^(?P<tag_pk>\d+)/acl/holder/new/$', 'tag_new_holder', (), 'tag_new_holder'),     
)
