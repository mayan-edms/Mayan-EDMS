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

urlpatterns_events = [
    url(regex=r'^events/$', view=EventListView.as_view(), name='events_list'),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/events/$',
        view=ObjectEventListView.as_view(), name='events_for_object'
    ),
    url(
        regex=r'^verbs/(?P<verb>[\w\-\.]+)/$',
        view=VerbEventListView.as_view(), name='events_by_verb'
    ),
    url(
        regex=r'^user/events/$', name='current_user_events',
        view=CurrentUserEventListView.as_view()
    ),
]

urlpatterns_notification = [
    url(
        regex=r'^user/notifications/$', view=NotificationListView.as_view(),
        name='user_notifications_list'
    ),
    url(
        regex=r'^user/notifications/(?P<pk>\d+)/mark_read/$',
        view=NotificationMarkRead.as_view(), name='notification_mark_read'
    ),
    url(
        regex=r'^user/notifications/all/mark_read/$',
        view=NotificationMarkReadAll.as_view(), name='notification_mark_read_all'
    ),
]

urlpatterns_subscriptions = [
    url(
        regex=r'^user/event_types/subscriptions/$',
        view=EventTypeSubscriptionListView.as_view(),
        name='event_types_user_subcriptions_list'
    ),
    url(
        regex=r'^user/object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/subscriptions/$',
        view=ObjectEventTypeSubscriptionListView.as_view(),
        name='object_event_types_user_subcriptions_list'
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_events)
urlpatterns.extend(urlpatterns_notification)
urlpatterns.extend(urlpatterns_subscriptions)

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
