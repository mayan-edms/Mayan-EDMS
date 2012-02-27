from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('acls.views',
    url(r'^new_holder_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_new_holder_for', (), 'acl_new_holder_for'),
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/$', 'acl_list', (), 'acl_list'),
    url(r'^details/(?P<access_object_gid>[.\w]+)/holder/(?P<holder_object_gid>[.\w]+)/$', 'acl_detail', (), 'acl_detail'),
    url(r'^holder/new/(?P<access_object_gid>[.\w]+)/$', 'acl_holder_new', (), 'acl_holder_new'),

    url(r'^multiple/grant/$', 'acl_grant', (), 'acl_multiple_grant'),
    url(r'^multiple/revoke/$', 'acl_revoke', (), 'acl_multiple_revoke'),

    url(r'^class/$', 'acl_setup_valid_classes', (), 'acl_setup_valid_classes'),
    url(r'^class/details/(?P<access_object_class_gid>[.\w]+)/holder/(?P<holder_object_gid>[.\w]+)/$', 'acl_class_acl_detail', (), 'acl_class_acl_detail'),
    url(r'^class/list_for/(?P<access_object_class_gid>[.\w]+)/$', 'acl_class_acl_list', (), 'acl_class_acl_list'),
    url(r'^class/holder/new/(?P<access_object_class_gid>[.\w]+)/$', 'acl_class_new_holder_for', (), 'acl_class_new_holder_for'),

    url(r'^class/multiple/grant/$', 'acl_class_multiple_grant', (), 'acl_class_multiple_grant'),
    url(r'^class/multiple/revoke/$', 'acl_class_multiple_revoke', (), 'acl_class_multiple_revoke'),

)
