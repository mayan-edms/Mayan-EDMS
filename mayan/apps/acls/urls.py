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
        regex=r'^acls/(?P<acl_id>\d+)/delete/$', name='acl_delete',
        view=ACLDeleteView.as_view()
    ),
    url(
        regex=r'^acls/(?P<acl_id>\d+)/permissions/$', name='acl_permissions',
        view=ACLPermissionsView.as_view()
    ),
    url(
        regex=r'^apps/(?P<app_label>[-\w]+)/models/(?P<model_name>[-\w]+)/objects/(?P<object_id>\d+)/acls/$',
        name='acl_list', view=ACLListView.as_view()
    ),
    url(
        regex=r'^apps/(?P<app_label>[-\w]+)/models/(?P<model_name>[-\w]+)/objects/(?P<object_id>\d+)/acls/create/$',
        name='acl_create', view=ACLCreateView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/acls/$',
        name='accesscontrollist-list', view=APIObjectACLListView.as_view()
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/$',
        name='accesscontrollist-detail', view=APIObjectACLView.as_view()
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/permissions/$',
        name='accesscontrollist-permission-list',
        view=APIObjectACLPermissionListView.as_view()
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/acls/(?P<pk>\d+)/permissions/(?P<permission_pk>\d+)/$',
        name='accesscontrollist-permission-detail',
        view=APIObjectACLPermissionView.as_view()
    ),
]
