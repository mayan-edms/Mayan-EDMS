from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIEventListView, APIEventTypeListView, APIEventTypeNamespaceDetailView,
    APIEventTypeNamespaceEventTypeListView, APIEventTypeNamespaceListView,
    APINotificationListView, APIObjectEventListView
)
from .views import (
    CurrentUserEventListView, EventListView, EventTypeSubscriptionListView,
    NotificationListView, NotificationMarkRead, NotificationMarkReadAll,
    ObjectEventListView, ObjectEventTypeSubscriptionListView,
    VerbEventListView
)

urlpatterns = [
    url(regex=r'^all/$', view=EventListView.as_view(), name='events_list'),
    url(
        regex=r'^for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        view=ObjectEventListView.as_view(), name='events_for_object'
    ),
    url(
        regex=r'^by_verb/(?P<verb>[\w\-\.]+)/$',
        view=VerbEventListView.as_view(), name='events_by_verb'
    ),
    url(
        regex=r'^notifications/(?P<pk>\d+)/mark_read/$',
        view=NotificationMarkRead.as_view(), name='notification_mark_read'
    ),
    url(
        regex=r'^notifications/all/mark_read/$',
        view=NotificationMarkReadAll.as_view(), name='notification_mark_read_all'
    ),
    url(
        regex=r'^user/events/$', name='current_user_events',
        view=CurrentUserEventListView.as_view()
    ),
    url(
        regex=r'^user/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/subscriptions/$',
        view=ObjectEventTypeSubscriptionListView.as_view(),
        name='object_event_types_user_subcriptions_list'
    ),
    url(
        regex=r'^user/event_types/subscriptions/$',
        view=EventTypeSubscriptionListView.as_view(),
        name='event_types_user_subcriptions_list'
    ),
    url(
        regex=r'^user/notifications/$', view=NotificationListView.as_view(),
        name='user_notifications_list'
    ),
]

api_urls = [
    url(
        regex=r'^event_type_namespaces/(?P<name>[-\w]+)/$',
        view=APIEventTypeNamespaceDetailView.as_view(),
        name='event-type-namespace-detail'
    ),
    url(
        regex=r'^event_type_namespaces/(?P<name>[-\w]+)/event_types/$',
        view=APIEventTypeNamespaceEventTypeListView.as_view(),
        name='event-type-namespace-event-type-list'
    ),
    url(
        regex=r'^event_type_namespaces/$',
        view=APIEventTypeNamespaceListView.as_view(),
        name='event-type-namespace-list'
    ),
    url(
        regex=r'^event_types/$', view=APIEventTypeListView.as_view(),
        name='event-type-list'
    ),
    url(regex=r'^events/$', view=APIEventListView.as_view(), name='event-list'),
    url(
        regex=r'^notifications/$', view=APINotificationListView.as_view(),
        name='notification-list'
    ),
    url(
        regex=r'^objects/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/events/$',
        view=APIObjectEventListView.as_view(), name='object-event-list'
    ),
]
