from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    MessageCreateView, MessageDeleteView, MessageEditView, MessageListView
)

urlpatterns = patterns(
    '',
    url(r'^list/$', MessageListView.as_view(), name='message_list'),
    url(r'^create/$', MessageCreateView.as_view(), name='message_create'),
    url(
        r'^(?P<pk>\d+)/edit/$', MessageEditView.as_view(), name='message_edit'
    ),
    url(
        r'^(?P<pk>\d+)/delete/$', MessageDeleteView.as_view(),
        name='message_delete'
    ),
)
