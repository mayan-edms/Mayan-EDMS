from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import MessageAPIViewSet
from .views import (
    MessageCreateView, MessageDeleteView, MessageEditView, MessageListView
)

urlpatterns = [
    url(
        regex=r'^messages/$', name='message_list',
        view=MessageListView.as_view()
    ),
    url(
        regex=r'^messages/create/$', name='message_create',
        view=MessageCreateView.as_view()
    ),
    url(
        regex=r'^messages/(?P<message_id>\d+)/delete/$',
        name='message_delete', view=MessageDeleteView.as_view()
    ),
    url(
        regex=r'^messages/(?P<message_id>\d+)/edit/$', name='message_edit',
        view=MessageEditView.as_view()
    )
]


api_router_entries = (
    {
        'prefix': r'messages', 'viewset': MessageAPIViewSet,
        'basename': 'message'
    },
)
