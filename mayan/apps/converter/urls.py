from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'converter.views',
    url(r'^create_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$', 'transformation_create', name='transformation_create'),
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$', 'transformation_list', name='transformation_list'),
    url(r'^delete/(?P<object_id>\d+)/$', 'transformation_delete', name='transformation_delete'),
    url(r'^edit/(?P<object_id>\d+)/$', 'transformation_edit', name='transformation_edit'),
)
