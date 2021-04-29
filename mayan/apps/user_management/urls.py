from django.conf.urls import url

from .api_views import (
    APICurrentUserView, APIGroupDetailView, APIGroupListView,
    APIGroupUserAddView, APIGroupUserListView, APIGroupUserRemoveView,
    APIUserDetailView, APIUserGroupListView, APIUserListView
)
from .views import (
    CurrentUserDetailsView, CurrentUserEditView, GroupCreateView,
    GroupDeleteView, GroupEditView, GroupListView, GroupUsersView,
    UserCreateView, UserDeleteView, UserDetailsView, UserEditView,
    UserGroupsView, UserListView, UserOptionsEditView
)

urlpatterns_current_user = [
    url(
        regex=r'^user/$', name='current_user_details',
        view=CurrentUserDetailsView.as_view()
    ),
    url(
        regex=r'^user/edit/$', name='current_user_edit',
        view=CurrentUserEditView.as_view()
    )
]

urlpatterns_groups = [
    url(
        regex=r'^groups/$', name='group_list', view=GroupListView.as_view()
    ),
    url(
        regex=r'^groups/create/$', name='group_create',
        view=GroupCreateView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/delete/$', name='group_delete',
        view=GroupDeleteView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/edit/$', name='group_edit',
        view=GroupEditView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>\d+)/users/$', name='group_members',
        view=GroupUsersView.as_view()
    )
]

urlpatterns_users = [
    url(regex=r'^users/$', name='user_list', view=UserListView.as_view()),
    url(
        regex=r'^users/create/$', name='user_create',
        view=UserCreateView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/delete/$', name='user_delete',
        view=UserDeleteView.as_view()
    ),
    url(
        regex=r'^users/multiple/delete/$', name='user_multiple_delete',
        view=UserDeleteView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/$', name='user_details',
        view=UserDetailsView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/edit/$', name='user_edit',
        view=UserEditView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/groups/$', name='user_groups',
        view=UserGroupsView.as_view()
    ),
    url(
        regex=r'^users/(?P<user_id>\d+)/options/$', name='user_options',
        view=UserOptionsEditView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_groups)
urlpatterns.extend(urlpatterns_current_user)
urlpatterns.extend(urlpatterns_users)

api_urls = [
    url(regex=r'^groups/$', view=APIGroupListView.as_view(), name='group-list'),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/$', view=APIGroupDetailView.as_view(),
        name='group-detail'
    ),

    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/$',
        name='group-user-list',
        view=APIGroupUserListView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/add/$',
        name='group-user-add', view=APIGroupUserAddView.as_view()
    ),
    url(
        regex=r'^groups/(?P<group_id>[0-9]+)/users/remove/$',
        name='group-user-remove', view=APIGroupUserRemoveView.as_view()
    ),
    url(regex=r'^users/$', view=APIUserListView.as_view(), name='user-list'),
    url(
        regex=r'^users/(?P<user_id>[0-9]+)/$', view=APIUserDetailView.as_view(),
        name='user-detail'
    ),
    url(
        regex=r'^users/current/$', view=APICurrentUserView.as_view(),
        name='user-current'
    ),
    url(
        regex=r'^users/(?P<user_id>[0-9]+)/groups/$',
        view=APIUserGroupListView.as_view(), name='user-group-list'
    ),
]
