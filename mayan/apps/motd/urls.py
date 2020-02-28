from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import MessageAPIViewSet
from .views import (
    MessageCreateView, MessageDeleteView, MessageEditView, MessageListView
)

urlpatterns = [
    url(regex=r'^messages/$', view=MessageListView.as_view(), name='message_list'),
    url(
        regex=r'^messages/create/$', view=MessageCreateView.as_view(),
        name='message_create'
    ),
    url(
        regex=r'^messages/(?P<pk>\d+)/delete/$', view=MessageDeleteView.as_view(),
        name='message_delete'
    ),
    url(
        regex=r'^messages/(?P<pk>\d+)/edit/$', view=MessageEditView.as_view(),
        name='message_edit'
    ),
]


api_router_entries = (
    {
        'prefix': r'messages', 'viewset': MessageAPIViewSet,
        'basename': 'message'
    },
)
