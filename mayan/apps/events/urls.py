from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('events.views',
    url(r'^all/$', 'events_list', (), 'events_list'),
    url(r'^for_object/(?P<app_label>[\w\-]+)/(?P<module_name>[\w\-]+)/(?P<object_id>\d+)/$', 'events_list', (), 'events_for_object'),
    url(r'^by_verb/(?P<verb>[\w\-]+)/$', 'events_list', (), 'events_by_verb'),
)
