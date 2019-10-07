from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APIPermissionList, APIRoleListView, APIRoleView
from .views import (
    GroupRolesView, RoleCreateView, RoleDeleteView, RoleEditView,
    RoleListView, SetupRoleMembersView, SetupRolePermissionsView
)

urlpatterns = [
    url(
        regex=r'^groups/(?P<pk>\d+)/roles/$',
        view=GroupRolesView.as_view(), name='group_roles'
    ),
    url(regex=r'^roles/$', view=RoleListView.as_view(), name='role_list'),
    url(
        regex=r'^roles/create/$', view=RoleCreateView.as_view(),
        name='role_create'
    ),
    url(
        regex=r'^roles/(?P<pk>\d+)/delete/$', view=RoleDeleteView.as_view(),
        name='role_delete'
    ),
    url(
        regex=r'^roles/(?P<pk>\d+)/edit/$', view=RoleEditView.as_view(),
        name='role_edit'
    ),
    url(
        regex=r'^roles/(?P<pk>\d+)/groups/$',
        view=SetupRoleMembersView.as_view(), name='role_groups'
    ),
    url(
        regex=r'^roles/(?P<pk>\d+)/permissions/$',
        view=SetupRolePermissionsView.as_view(), name='role_permissions'
    ),
]

api_urls = [
    url(
        regex=r'^permissions/$', view=APIPermissionList.as_view(),
        name='permission-list'
    ),
    url(regex=r'^roles/$', view=APIRoleListView.as_view(), name='role-list'),
    url(
        regex=r'^roles/(?P<pk>[0-9]+)/$', view=APIRoleView.as_view(),
        name='role-detail'
    ),
]
