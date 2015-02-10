from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('mailer.views',
    url(r'^(?P<document_id>\d+)/send/link/$', 'send_document_link', (), 'send_document_link'),
    url(r'^(?P<document_id>\d+)/send/document/$', 'send_document_link', {'as_attachment': True}, 'send_document'),
)
