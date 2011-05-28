from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('history.views',
    url(r'^list/$', 'history_list', (), 'history_list'),
    url(r'^list/for_object/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<object_id>\d+)/$', 'history_for_object', (), 'history_for_object'),
    url(r'^(?P<object_id>\d+)/$', 'history_view', (), 'history_view'),
)

