from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIEventListView, APIEventTypeListView, APIEventTypeNamespaceDetailView,
    APIEventTypeNamespaceEventTypeListView, APIEventTypeNamespaceListView,
    APINotificationListView, APIObjectEventListView
)
from .views import (
    EventListView, EventTypeSubscriptionListView, NotificationListView,
    NotificationMarkRead, NotificationMarkReadAll, ObjectEventListView,
    ObjectEventTypeSubscriptionListView, VerbEventListView
)

urlpatterns = [
    url(r'^all/$', EventListView.as_view(), name='events_list'),
    url(
        r'^for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        ObjectEventListView.as_view(), name='events_for_object'
    ),
    url(
        r'^by_verb/(?P<verb>[\w\-\.]+)/$', VerbEventListView.as_view(),
        name='events_by_verb'
    ),
    url(
        r'^notifications/(?P<pk>\d+)/mark_read/$',
        NotificationMarkRead.as_view(), name='notification_mark_read'
    ),
    url(
        r'^notifications/all/mark_read/$',
        NotificationMarkReadAll.as_view(), name='notification_mark_read_all'
    ),
    url(
        r'^user/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/subscriptions/$',
        ObjectEventTypeSubscriptionListView.as_view(),
        name='object_event_types_user_subcriptions_list'
    ),
    url(
        r'^user/event_types/subscriptions/$',
        EventTypeSubscriptionListView.as_view(),
        name='event_types_user_subcriptions_list'
    ),
    url(
        r'^user/notifications/$',
        NotificationListView.as_view(),
        name='user_notifications_list'
    ),
]

api_urls = [
    url(
        r'^event_type_namespaces/(?P<name>[-\w]+)/$',
        APIEventTypeNamespaceDetailView.as_view(),
        name='event-type-namespace-detail'
    ),
    url(
        r'^event_type_namespaces/(?P<name>[-\w]+)/event_types/$',
        APIEventTypeNamespaceEventTypeListView.as_view(),
        name='event-type-namespace-event-type-list'
    ),
    url(
        r'^event_type_namespaces/$', APIEventTypeNamespaceListView.as_view(),
        name='event-type-namespace-list'
    ),
    url(
        r'^event_types/$', APIEventTypeListView.as_view(),
        name='event-type-list'
    ),
    url(r'^events/$', APIEventListView.as_view(), name='event-list'),
    url(
        r'^notifications/$', APINotificationListView.as_view(),
        name='notification-list'
    ),
    url(
        r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/events/$',
        APIObjectEventListView.as_view(), name='object-event-list'
    ),
]
