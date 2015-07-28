from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import EventListView, ObjectEventListView, VerbEventListView

urlpatterns = patterns(
    'events.views',
    url(r'^all/$', EventListView.as_view(), name='events_list'),
    url(
        r'^for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        ObjectEventListView.as_view(), name='events_for_object'
    ),
    url(
        r'^by_verb/(?P<verb>[\w\-]+)/$', VerbEventListView.as_view(),
        name='events_by_verb'
    ),
)
