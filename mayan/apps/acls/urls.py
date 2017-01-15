from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    ACLCreateView, ACLDeleteView, ACLListView, ACLPermissionsView
)

urlpatterns = [
    url(
        r'^(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/create/$',
        ACLCreateView.as_view(), name='acl_create'
    ),
    url(
        r'^(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/list/$',
        ACLListView.as_view(), name='acl_list'
    ),
    url(r'^(?P<pk>\d+)/delete/$', ACLDeleteView.as_view(), name='acl_delete'),
    url(
        r'^(?P<pk>\d+)/permissions/$', ACLPermissionsView.as_view(),
        name='acl_permissions'
    ),
]
