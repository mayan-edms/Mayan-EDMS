from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('acls.views',
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_list', (), 'acl_list'),
    #url(r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/holder/(?P<holder_app_label>[-\w]+)/(?P<holder_model_name>[-\w]+)/(?P<holder_id>\d+)/$', 'acl_detail', (), 'acl_detail'),
    url(r'^details/(?P<access_object_gid>[.\w]+)/holder/(?P<holder_object_gid>[.\w]+)/$', 'acl_detail', (), 'acl_detail'),
	
#    url(r'^role/list/$', 'role_list', (), 'role_list'),
#    url(r'^role/create/$', 'role_create', (), 'role_create'),
#    url(r'^role/(?P<role_id>\d+)/permissions/$', 'role_permissions', (), 'role_permissions'),
#    url(r'^role/(?P<role_id>\d+)/edit/$', 'role_edit', (), 'role_edit'),
#    url(r'^role/(?P<role_id>\d+)/delete/$', 'role_delete', (), 'role_delete'),
#    url(r'^role/(?P<role_id>\d+)/members/$', 'role_members', (), 'role_members'),
#   
    url(r'^multiple/grant/$', 'acl_grant', (), 'acl_multiple_grant'),
#    url(r'^permissions/multiple/revoke/$', 'permission_revoke', (), 'permission_multiple_revoke'),
)
