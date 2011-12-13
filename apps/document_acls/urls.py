from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('document_acls.views',
    url(r'^list_for/document/(?P<document_id>\d+)/$', 'document_acl_list', (), 'document_acl_list'),
    url(r'^new_holder_for/document/(?P<document_id>\d+)/$', 'document_new_holder', (), 'document_new_holder'),
)
