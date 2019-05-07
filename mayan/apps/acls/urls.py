from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIObjectACLListView, APIObjectACLPermissionListView,
    APIObjectACLPermissionView, APIObjectACLView
)
from .views import (
    ACLCreateView, ACLDeleteView, ACLListView, ACLPermissionsView
)

urlpatterns = [
    url(
        regex=r'^(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/create/$',
        view=ACLCreateView.as_view(), name='acl_create'
    ),
    url(
        regex=r'^(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/list/$',
        view=ACLListView.as_view(), name='acl_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$', view=ACLDeleteView.as_view(),
        name='acl_delete'
    ),
    url(
        regex=r'^(?P<pk>\d+)/permissions/$', view=ACLPermissionsView.as_view(),
        name='acl_permissions'
    ),
]

api_urls = [
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/acls/$',
        view=APIObjectACLListView.as_view(), name='accesscontrollist-list'
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/$',
        view=APIObjectACLView.as_view(), name='accesscontrollist-detail'
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/permissions/$',
        view=APIObjectACLPermissionListView.as_view(),
        name='accesscontrollist-permission-list'
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/permissions/(?P<permission_pk>\d+)/$',
        view=APIObjectACLPermissionView.as_view(),
        name='accesscontrollist-permission-detail'
    ),
]
