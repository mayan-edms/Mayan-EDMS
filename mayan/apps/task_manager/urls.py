from __future__ import unicode_literals

from django.conf.urls import url

from .views import QueueListView

urlpatterns = [
    url(
        regex=r'^queues/$', view=QueueListView.as_view(),
        name='queue_list'
    ),
]
