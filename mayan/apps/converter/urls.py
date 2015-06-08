from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'converter.views',
    url(r'^create_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$', 'transformation_create', (), 'transformation_create'),
    url(r'^list_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$', 'transformation_list', (), 'transformation_list'),
    url(r'^delete/(?P<object_id>\d+)/$', 'transformation_delete', (), 'transformation_delete'),
    url(r'^edit/(?P<object_id>\d+)/$', 'transformation_edit', (), 'transformation_edit'),
)
