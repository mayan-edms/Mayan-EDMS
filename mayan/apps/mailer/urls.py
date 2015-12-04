from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import LogEntryListView

urlpatterns = patterns(
    'mailer.views',
    url(
        r'^(?P<document_id>\d+)/send/link/$', 'send_document_link',
        name='send_document_link'
    ),
    url(
        r'^(?P<document_id>\d+)/send/document/$', 'send_document_link',
        {'as_attachment': True}, name='send_document'
    ),
    url(
        r'^log/$', LogEntryListView.as_view(), name='error_log'
    ),
)
