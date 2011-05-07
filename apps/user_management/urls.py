from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('user_management.views',
    url(r'^list/$', 'user_list', (), 'user_list'),
    url(r'^add/$', 'user_add', (), 'user_add'),
    url(r'^(?P<user_id>\d+)/edit/$', 'user_edit', (), 'user_edit'),
    url(r'^(?P<user_id>\d+)/delete/$', 'user_delete', (), 'user_delete'),
    url(r'^multiple/delete/$', 'user_multiple_delete', (), 'user_multiple_delete'),
    url(r'^(?P<user_id>\d+)/set_password/$', 'user_set_password', (), 'user_set_password'),
    url(r'^multiple/set_password/$', 'user_multiple_set_password', (), 'user_multiple_set_password'),
)
