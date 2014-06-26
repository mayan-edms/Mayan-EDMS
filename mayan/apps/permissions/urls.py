from __future__ import absolute_import

from django.conf.urls import patterns, url

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
