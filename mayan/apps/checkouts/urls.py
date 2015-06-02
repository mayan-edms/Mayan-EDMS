from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import APICheckedoutDocumentListView, APICheckedoutDocumentView
from .views import CheckoutListView

urlpatterns = patterns(
    'checkouts.views',
    url(r'^list/$', CheckoutListView.as_view(), name='checkout_list'),
    url(r'^(?P<document_pk>\d+)/check/out/$', 'checkout_document', name='checkout_document'),
    url(r'^(?P<document_pk>\d+)/check/in/$', 'checkin_document', name='checkin_document'),
    url(r'^(?P<document_pk>\d+)/check/info/$', 'checkout_info', name='checkout_info'),
)

api_urls = patterns(
    '',
    url(r'^documents/$', APICheckedoutDocumentListView.as_view(), name='checkout-document-list'),
    url(r'^documents/(?P<pk>[0-9]+)/$', APICheckedoutDocumentView.as_view(), name='checkedout-document-view'),
)
