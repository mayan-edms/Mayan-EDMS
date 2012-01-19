from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('permissions.views',
    url(r'^role/list/$', 'role_list', (), 'role_list'),
    url(r'^role/create/$', 'role_create', (), 'role_create'),
    url(r'^role/(?P<role_id>\d+)/permissions/$', 'role_permissions', (), 'role_permissions'),
    url(r'^role/(?P<role_id>\d+)/edit/$', 'role_edit', (), 'role_edit'),
    url(r'^role/(?P<role_id>\d+)/delete/$', 'role_delete', (), 'role_delete'),
    url(r'^role/(?P<role_id>\d+)/members/$', 'role_members', (), 'role_members'),

    url(r'^permissions/multiple/grant/$', 'permission_grant', (), 'permission_multiple_grant'),
    url(r'^permissions/multiple/revoke/$', 'permission_revoke', (), 'permission_multiple_revoke'),
)
