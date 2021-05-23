from django.conf.urls import url

from .views import (
    MessageCreateView, MessageDeleteView, MessageDetailView, MessageListView,
    MessageMarkReadAllView, MessageMarkReadView, MessageMarkUnReadView
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
        name='message_single_delete', view=MessageDeleteView.as_view()
    ),
    url(
        regex=r'^messages/(?P<message_id>\d+)/details/$',
        name='message_detail', view=MessageDetailView.as_view()
    ),
    url(
        regex=r'^messages/multiple/delete/$',
        name='message_multiple_delete', view=MessageDeleteView.as_view()
    ),
    url(
        regex=r'^messages/mark_read/$',
        name='message_multiple_mark_read', view=MessageMarkReadView.as_view()
    ),
    url(
        regex=r'^messages/mark_unread/$',
        name='message_multiple_mark_unread',
        view=MessageMarkUnReadView.as_view()
    ),
    url(
        regex=r'^messages/(?P<message_id>\d+)/mark_read/$',
        name='message_single_mark_read', view=MessageMarkReadView.as_view()
    ),
    url(
        regex=r'^messages/(?P<message_id>\d+)/mark_unread/$',
        name='message_single_mark_unread',
        view=MessageMarkUnReadView.as_view()
    ),
    url(
        regex=r'^messages/all/mark_read/$',
        name='message_all_mark_read',
        view=MessageMarkReadAllView.as_view()
    ),
]
