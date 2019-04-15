from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APICheckedoutDocumentListView, APICheckedoutDocumentView
from .views import (
    CheckoutDocumentView, CheckoutDetailView, CheckoutListView,
    DocumentCheckinView
)

urlpatterns = [
    url(
        regex=r'^list/$', view=CheckoutListView.as_view(), name='check_out_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/check/out/$', view=CheckoutDocumentView.as_view(),
        name='check_out_document'
    ),
    url(
        regex=r'^(?P<pk>\d+)/check/in/$', view=DocumentCheckinView.as_view(),
        name='check_in_document'
    ),
    url(
        regex=r'^(?P<pk>\d+)/check/info/$', view=CheckoutDetailView.as_view(),
        name='check_out_info'
    ),
]

api_urls = [
    url(
        regex=r'^checkouts/$', view=APICheckedoutDocumentListView.as_view(),
        name='checkout-document-list'
    ),
    url(
        regex=r'^checkouts/(?P<pk>[0-9]+)/checkout_info/$',
        view=APICheckedoutDocumentView.as_view(),
        name='checkedout-document-view'
    ),
]
