from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APICurrentUserView, APIGroupListView, APIGroupView, APIUserGroupList,
    APIUserListView, APIUserView
)
from .views import (
    CurrentUserDetailsView, CurrentUserEditView, GroupCreateView,
    GroupDeleteView, GroupEditView, GroupListView, GroupUsersView,
    UserCreateView, UserDeleteView, UserDetailsView, UserEditView,
    UserGroupsView, UserListView, UserOptionsEditView
)

urlpatterns_current_user = [
    url(
        regex=r'^user/$', view=CurrentUserDetailsView.as_view(),
        name='current_user_details'
    ),
    url(
        regex=r'^user/edit/$', view=CurrentUserEditView.as_view(),
        name='current_user_edit'
    )
]

urlpatterns_groups = [
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
        regex=r'^group/(?P<pk>\d+)/users/$', view=GroupUsersView.as_view(),
        name='group_members'
    )
]

urlpatterns_users = [
    url(regex=r'^users/$', view=UserListView.as_view(), name='user_list'),
    url(
        regex=r'^users/create/$', view=UserCreateView.as_view(),
        name='user_create'
    ),
    url(
        regex=r'^users/(?P<pk>\d+)/delete/$', view=UserDeleteView.as_view(),
        name='user_delete'
    ),
    url(
        regex=r'^users/multiple/delete/$', view=UserDeleteView.as_view(),
        name='user_multiple_delete'
    ),
    url(
        regex=r'^users/(?P<pk>\d+)/$', view=UserDetailsView.as_view(),
        name='user_details'
    ),
    url(
        regex=r'^users/(?P<pk>\d+)/edit/$', view=UserEditView.as_view(),
        name='user_edit'
    ),
    url(
        regex=r'^users/(?P<pk>\d+)/groups/$', view=UserGroupsView.as_view(),
        name='user_groups'
    ),
    url(
        regex=r'^users/(?P<pk>\d+)/options/$',
        view=UserOptionsEditView.as_view(), name='user_options'
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_groups)
urlpatterns.extend(urlpatterns_current_user)
urlpatterns.extend(urlpatterns_users)

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
