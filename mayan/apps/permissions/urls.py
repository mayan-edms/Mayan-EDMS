from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import APIRoleListView, APIRoleView
from .views import RoleCreateView, RoleDeleteView, RoleEditView

urlpatterns = patterns('permissions.views',
    url(r'^role/list/$', 'role_list', (), 'role_list'),
    url(r'^role/create/$', RoleCreateView.as_view(), name='role_create'),
    url(r'^role/(?P<role_id>\d+)/permissions/$', 'role_permissions', (), 'role_permissions'),
    url(r'^role/(?P<pk>\d+)/edit/$', RoleEditView.as_view(), name='role_edit'),
    url(r'^role/(?P<pk>\d+)/delete/$', RoleDeleteView.as_view(), name='role_delete'),
    url(r'^role/(?P<role_id>\d+)/members/$', 'role_members', (), 'role_members'),

    url(r'^permissions/multiple/grant/$', 'permission_grant', (), 'permission_multiple_grant'),
    url(r'^permissions/multiple/revoke/$', 'permission_revoke', (), 'permission_multiple_revoke'),
)

api_urls = patterns('',
    url(r'^roles/$', APIRoleListView.as_view(), name='role-list'),
    url(r'^roles/(?P<pk>[0-9]+)/$', APIRoleView.as_view(), name='role-detail'),
)
