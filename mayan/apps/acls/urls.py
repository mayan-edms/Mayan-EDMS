from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'acls.views',
    url(r'^new_holder_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_new_holder_for', name='acl_new_holder_for'),
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_list', name='acl_list'),
    url(r'^details/(?P<access_object_gid>[.\w]+)/holder/(?P<holder_object_gid>[.\w]+)/$', 'acl_detail', name='acl_detail'),
    url(r'^holder/new/(?P<access_object_gid>[.\w]+)/$', 'acl_holder_new', name='acl_holder_new'),

    url(r'^multiple/grant/$', 'acl_grant', name='acl_multiple_grant'),
    url(r'^multiple/revoke/$', 'acl_revoke', name='acl_multiple_revoke'),
)
