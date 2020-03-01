from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import CurrentUserAPIView, GroupAPIViewSet, UserAPIViewSet
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
        regex=r'^users/(?P<pk>\d+)/delete/$', name='user_delete',
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
    url(
        regex=r'^users/current/$', name='user-current',
        view=CurrentUserAPIView.as_view()
    ),
]
api_router_entries = (
    {'prefix': r'groups', 'viewset': GroupAPIViewSet, 'basename': 'group'},
    {'prefix': r'users', 'viewset': UserAPIViewSet, 'basename': 'user'},
)
