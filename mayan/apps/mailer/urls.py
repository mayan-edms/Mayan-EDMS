from __future__ import unicode_literals

from django.conf.urls import url

from .views import LogEntryListView, MailDocumentLinkView, MailDocumentView

urlpatterns = [
    url(
        r'^(?P<pk>\d+)/send/link/$', MailDocumentLinkView.as_view(),
        name='send_document_link'
    ),
    url(
        r'^multiple/send/link/$', MailDocumentLinkView.as_view(),
        name='send_multiple_document_link'
    ),
    url(
        r'^(?P<pk>\d+)/send/document/$', MailDocumentView.as_view(),
        name='send_document'
    ),
    url(
        r'^multiple/send/document/$', MailDocumentView.as_view(),
        name='send_multiple_document'
    ),
    url(
        r'^log/$', LogEntryListView.as_view(), name='error_log'
    ),
]
