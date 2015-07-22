from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import APIRoleListView, APIRoleView
from .views import (
    RoleCreateView, RoleDeleteView, RoleEditView, RoleListView,
    SetupRoleMembersView, SetupRolePermissionsView
)

urlpatterns = patterns(
    'permissions.views',
    url(r'^role/list/$', RoleListView.as_view(), name='role_list'),
    url(r'^role/create/$', RoleCreateView.as_view(), name='role_create'),
    url(
        r'^role/(?P<pk>\d+)/permissions/$', SetupRolePermissionsView.as_view(),
        name='role_permissions'
    ),
    url(r'^role/(?P<pk>\d+)/edit/$', RoleEditView.as_view(), name='role_edit'),
    url(
        r'^role/(?P<pk>\d+)/delete/$', RoleDeleteView.as_view(),
        name='role_delete'
    ),
    url(
        r'^role/(?P<pk>\d+)/members/$', SetupRoleMembersView.as_view(),
        name='role_members'
    ),
)

api_urls = patterns(
    '',
    url(r'^roles/$', APIRoleListView.as_view(), name='role-list'),
    url(r'^roles/(?P<pk>[0-9]+)/$', APIRoleView.as_view(), name='role-detail'),
)
