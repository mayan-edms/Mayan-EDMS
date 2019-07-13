from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APICheckedoutDocumentListView, APICheckedoutDocumentView
from .views import (
    DocumentCheckinView, DocumentCheckoutDetailView, DocumentCheckoutView,
    DocumentCheckoutListView
)

urlpatterns = [
    url(
        regex=r'^documents/$', view=DocumentCheckoutListView.as_view(),
        name='check_out_list'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/check_in/$', view=DocumentCheckinView.as_view(),
        name='check_in_document'
    ),
    url(
        regex=r'^documents/multiple/check_in/$',
        name='check_in_document_multiple', view=DocumentCheckinView.as_view()
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/check_out/$', view=DocumentCheckoutView.as_view(),
        name='check_out_document'
    ),
    url(
        regex=r'^documents/multiple/check_out/$',
        name='check_out_document_multiple', view=DocumentCheckoutView.as_view()
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/checkout/info/$',
        view=DocumentCheckoutDetailView.as_view(), name='check_out_info'
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
