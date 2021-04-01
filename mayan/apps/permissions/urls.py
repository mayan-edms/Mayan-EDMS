from django.conf.urls import url

from .api_views import (
    APIPermissionList, APIRoleDetailView, APIRoleGroupAddView,
    APIRoleGroupListView, APIRoleGroupRemoveView, APIRoleListView,
    APIRolePermissionAddView, APIRolePermissionListView,
    APIRolePermissionRemoveView
)

from .views import (
    GroupRolesView, RoleCreateView, RoleDeleteView, RoleEditView,
    RoleListView, SetupRoleMembersView, SetupRolePermissionsView
)

urlpatterns = [
    url(
        regex=r'^groups/(?P<group_id>\d+)/roles/$', name='group_roles',
        view=GroupRolesView.as_view()
    ),
    url(regex=r'^roles/$', name='role_list', view=RoleListView.as_view()),
    url(
        regex=r'^roles/create/$', name='role_create',
        view=RoleCreateView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>\d+)/delete/$', name='role_delete',
        view=RoleDeleteView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>\d+)/edit/$', name='role_edit',
        view=RoleEditView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>\d+)/groups/$', name='role_groups',
        view=SetupRoleMembersView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>\d+)/permissions/$',
        name='role_permissions', view=SetupRolePermissionsView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^permissions/$', name='permission-list',
        view=APIPermissionList.as_view()
    ),
    url(regex=r'^roles/$', name='role-list', view=APIRoleListView.as_view()),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/$', name='role-detail',
        view=APIRoleDetailView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/groups/$', name='role-group-list',
        view=APIRoleGroupListView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/groups/add/$',
        name='role-group-add', view=APIRoleGroupAddView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/groups/remove/$',
        name='role-group-remove', view=APIRoleGroupRemoveView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/permissions/$',
        name='role-permission-list', view=APIRolePermissionListView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/permissions/add/$',
        name='role-permission-add', view=APIRolePermissionAddView.as_view()
    ),
    url(
        regex=r'^roles/(?P<role_id>[0-9]+)/permissions/remove/$',
        name='role-permission-remove',
        view=APIRolePermissionRemoveView.as_view()
    ),

]
