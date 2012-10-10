from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('tags.views',
    url(r'^list/$', 'tag_list', (), 'tag_list'),
    url(r'^create/$', 'tag_create', (), 'tag_create'),
    url(r'^(?P<tag_id>\d+)/delete/$', 'tag_delete', (), 'tag_delete'),
    url(r'^(?P<tag_id>\d+)/edit/$', 'tag_edit', (), 'tag_edit'),
    url(r'^(?P<tag_id>\d+)/tagged_item/list/$', 'tag_tagged_item_list', (), 'tag_tagged_item_list'),
    url(r'^multiple/delete/$', 'tag_multiple_delete', (), 'tag_multiple_delete'),

    url(r'^multiple/remove/document/(?P<document_id>\d+)/$', 'single_document_multiple_tag_remove', (), 'single_document_multiple_tag_remove'),
    url(r'^multiple/remove/document/multiple/$', 'multiple_documents_selection_tag_remove', (), 'multiple_documents_selection_tag_remove'),

    url(r'^selection/attach/document/(?P<document_id>\d+)/$', 'tag_attach', (), 'tag_attach'),
    url(r'^selection/attach/document/multiple/$', 'tag_multiple_attach', (), 'tag_multiple_attach'),
    
    url(r'^for/document/(?P<document_id>\d+)/$', 'document_tags', (), 'document_tags'),

    url(r'^(?P<tag_pk>\d+)/acl/list/$', 'tag_acl_list', (), 'tag_acl_list'),
)
