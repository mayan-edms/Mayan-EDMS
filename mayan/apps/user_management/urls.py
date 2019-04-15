from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APICurrentUserView, APIGroupListView, APIGroupView, APIUserGroupList,
    APIUserListView, APIUserView
)
from .views import (
    GroupCreateView, GroupDeleteView, GroupEditView, GroupListView,
    GroupMembersView, UserCreateView, UserDeleteView, UserEditView,
    UserGroupsView, UserListView, UserOptionsEditView, UserSetPasswordView
)

urlpatterns = [
    url(
        regex=r'^group/list/$', view=GroupListView.as_view(), name='group_list'
    ),
    url(
        regex=r'^group/create/$', view=GroupCreateView.as_view(),
        name='group_create'
    ),
    url(
        regex=r'^group/(?P<pk>\d+)/edit/$', view=GroupEditView.as_view(),
        name='group_edit'
    ),
    url(
        regex=r'^group/(?P<pk>\d+)/delete/$', view=GroupDeleteView.as_view(),
        name='group_delete'
    ),
    url(
        regex=r'^group/(?P<pk>\d+)/members/$', view=GroupMembersView.as_view(),
        name='group_members'
    ),

    url(regex=r'^user/list/$', view=UserListView.as_view(), name='user_list'),
    url(
        regex=r'^user/create/$', view=UserCreateView.as_view(),
        name='user_create'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/edit/$', view=UserEditView.as_view(),
        name='user_edit'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/delete/$', view=UserDeleteView.as_view(),
        name='user_delete'
    ),
    url(
        regex=r'^user/multiple/delete/$', view=UserDeleteView.as_view(),
        name='user_multiple_delete'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/set_password/$',
        view=UserSetPasswordView.as_view(), name='user_set_password'
    ),
    url(
        regex=r'^user/multiple/set_password/$',
        view=UserSetPasswordView.as_view(), name='user_multiple_set_password'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/groups/$', view=UserGroupsView.as_view(),
        name='user_groups'
    ),
    url(
        regex=r'^user/(?P<pk>\d+)/options/$',
        view=UserOptionsEditView.as_view(), name='user_options'
    ),
]

api_urls = [
    url(regex=r'^groups/$', view=APIGroupListView.as_view(), name='group-list'),
    url(
        regex=r'^groups/(?P<pk>[0-9]+)/$', view=APIGroupView.as_view(),
        name='group-detail'
    ),
    url(regex=r'^users/$', view=APIUserListView.as_view(), name='user-list'),
    url(
        regex=r'^users/(?P<pk>[0-9]+)/$', view=APIUserView.as_view(),
        name='user-detail'
    ),
    url(
        regex=r'^users/current/$', view=APICurrentUserView.as_view(),
        name='user-current'
    ),
    url(
        regex=r'^users/(?P<pk>[0-9]+)/groups/$',
        view=APIUserGroupList.as_view(), name='users-group-list'
    ),
]
