from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import APICheckedoutDocumentListView, APICheckedoutDocumentView

urlpatterns = patterns('checkouts.views',
    url(r'^list/$', 'checkout_list', (), 'checkout_list'),
    url(r'^(?P<document_pk>\d+)/check/out/$', 'checkout_document', (), 'checkout_document'),
    url(r'^(?P<document_pk>\d+)/check/in/$', 'checkin_document', (), 'checkin_document'),
    url(r'^(?P<document_pk>\d+)/check/info/$', 'checkout_info', (), 'checkout_info'),
)

api_urls = patterns('',
    url(r'^documents/$', APICheckedoutDocumentListView.as_view(), name='checkout-document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', APICheckedoutDocumentView.as_view(), name='checkedout-document-view'),
)
