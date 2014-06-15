from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('user_management.views',
    url(r'^user/list/$', 'user_list', (), 'user_list'),
    url(r'^user/add/$', 'user_add', (), 'user_add'),
    url(r'^user/(?P<user_id>\d+)/edit/$', 'user_edit', (), 'user_edit'),
    url(r'^user/(?P<user_id>\d+)/delete/$', 'user_delete', (), 'user_delete'),
    url(r'^user/multiple/delete/$', 'user_multiple_delete', (), 'user_multiple_delete'),
    url(r'^user/(?P<user_id>\d+)/set_password/$', 'user_set_password', (), 'user_set_password'),
    url(r'^user/multiple/set_password/$', 'user_multiple_set_password', (), 'user_multiple_set_password'),
    url(r'^user/(?P<user_id>\d+)/groups/$', 'user_groups', (), 'user_groups'),

    url(r'^group/list/$', 'group_list', (), 'group_list'),
    url(r'^group/add/$', 'group_add', (), 'group_add'),
    url(r'^group/(?P<group_id>\d+)/edit/$', 'group_edit', (), 'group_edit'),
    url(r'^group/(?P<group_id>\d+)/delete/$', 'group_delete', (), 'group_delete'),
    url(r'^group/multiple/delete/$', 'group_multiple_delete', (), 'group_multiple_delete'),
    url(r'^group/(?P<group_id>\d+)/members/$', 'group_members', (), 'group_members'),
)
