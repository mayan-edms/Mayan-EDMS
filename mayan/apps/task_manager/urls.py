from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    QueueListView, QueueActiveTaskListView, QueueScheduledTaskListView,
    QueueReservedTaskListView
)


urlpatterns = [
    url(
        regex=r'^queues/$', view=QueueListView.as_view(),
        name='queue_list'
    ),
    url(
        regex=r'^queues/(?P<queue_name>[-\w]+)/tasks/active/$',
        view=QueueActiveTaskListView.as_view(), name='queue_active_task_list'
    ),
    url(
        regex=r'^queues/(?P<queue_name>[-\w]+)/tasks/scheduled/$',
        view=QueueScheduledTaskListView.as_view(),
        name='queue_scheduled_task_list'
    ),
    url(
        regex=r'^queues/(?P<queue_name>[-\w]+)/tasks/reserved/$',
        view=QueueReservedTaskListView.as_view(),
        name='queue_reserved_task_list'
    ),
]
