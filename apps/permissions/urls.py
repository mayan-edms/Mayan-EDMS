from django.conf.urls.defaults import *

urlpatterns = patterns('permissions.views',
    url(r'^role/list/$', 'role_list', (), 'role_list'),
    url(r'^role/create/$', 'role_create', (), 'role_create'),
    url(r'^role/(?P<role_id>\d+)/permissions/$', 'role_permissions', (), 'role_permissions'),
    url(r'^role/(?P<role_id>\d+)/edit/$', 'role_edit', (), 'role_edit'),
    url(r'^role/(?P<role_id>\d+)/delete/$', 'role_delete', (), 'role_delete'),

    url(r'^permission/(?P<permission_id>\d+)/for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/grant/$', 'permission_grant_revoke', {'action':'grant'}, 'permission_grant'),
    url(r'^permission/(?P<permission_id>\d+)/for/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<pk>\d+)/revoke/$', 'permission_grant_revoke', {'action':'revoke'}, 'permission_revoke'),
)
