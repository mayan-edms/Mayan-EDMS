from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APIMessageListView, APIMessageView
from .views import (
    MessageCreateView, MessageDeleteView, MessageEditView, MessageListView
)

urlpatterns = [
    url(regex=r'^list/$', view=MessageListView.as_view(), name='message_list'),
    url(
        regex=r'^create/$', view=MessageCreateView.as_view(),
        name='message_create'
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/$', view=MessageEditView.as_view(),
        name='message_edit'
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$', view=MessageDeleteView.as_view(),
        name='message_delete'
    ),
]

api_urls = [
    url(
        regex=r'^messages/$', view=APIMessageListView.as_view(),
        name='message-list'
    ),
    url(
        regex=r'^messages/(?P<pk>[0-9]+)/$', view=APIMessageView.as_view(),
        name='message-detail'
    ),
]
