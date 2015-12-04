from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APICurrentUserView, APIGroupListView, APIGroupView, APIUserListView,
    APIUserView
)
from .views import (
    GroupCreateView, GroupDeleteView, GroupEditView, GroupListView,
    GroupMembersView, UserEditView, UserGroupsView, UserListView
)

urlpatterns = patterns(
    'user_management.views',
    url(r'^group/list/$', GroupListView.as_view(), name='group_list'),
    url(r'^group/add/$', GroupCreateView.as_view(), name='group_add'),
    url(
        r'^group/(?P<pk>\d+)/edit/$', GroupEditView.as_view(),
        name='group_edit'
    ),
    url(
        r'^group/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(),
        name='group_delete'
    ),
    url(
        r'^group/(?P<pk>\d+)/members/$', GroupMembersView.as_view(),
        name='group_members'
    ),

    url(r'^user/list/$', UserListView.as_view(), name='user_list'),
    url(r'^user/add/$', 'user_add', name='user_add'),
    url(r'^user/(?P<pk>\d+)/edit/$', UserEditView.as_view(), name='user_edit'),
    url(r'^user/(?P<user_id>\d+)/delete/$', 'user_delete', name='user_delete'),
    url(
        r'^user/multiple/delete/$', 'user_multiple_delete',
        name='user_multiple_delete'
    ),
    url(
        r'^user/(?P<user_id>\d+)/set_password/$', 'user_set_password',
        name='user_set_password'
    ),
    url(
        r'^user/multiple/set_password/$', 'user_multiple_set_password',
        name='user_multiple_set_password'
    ),
    url(
        r'^user/(?P<pk>\d+)/groups/$', UserGroupsView.as_view(),
        name='user_groups'
    ),
)

api_urls = patterns(
    '',
    url(r'^groups/$', APIGroupListView.as_view(), name='group-list'),
    url(
        r'^groups/(?P<pk>[0-9]+)/$', APIGroupView.as_view(),
        name='group-detail'
    ),
    url(r'^users/$', APIUserListView.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', APIUserView.as_view(), name='user-detail'),
    url(
        r'^users/current/$', APICurrentUserView.as_view(), name='user-current'
    ),
)
