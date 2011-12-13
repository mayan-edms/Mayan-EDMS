from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('acls.views',
    url(r'^new_holder_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_new_holder_for', (), 'acl_new_holder_for'),
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_list', (), 'acl_list'),
    #url(r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/holder/(?P<holder_app_label>[-\w]+)/(?P<holder_model_name>[-\w]+)/(?P<holder_id>\d+)/$', 'acl_detail', (), 'acl_detail'),
    url(r'^details/(?P<access_object_gid>[.\w]+)/holder/(?P<holder_object_gid>[.\w]+)/$', 'acl_detail', (), 'acl_detail'),
 
    url(r'^multiple/grant/$', 'acl_grant', (), 'acl_multiple_grant'),
    url(r'^multiple/revoke/$', 'acl_revoke', (), 'acl_multiple_revoke'),
)
