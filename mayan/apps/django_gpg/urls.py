from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APIKeyListView, APIKeyView
from .views import (
    KeyDeleteView, KeyDetailView, KeyDownloadView, KeyQueryView,
    KeyQueryResultView, KeyReceive, KeyUploadView, PrivateKeyListView,
    PublicKeyListView
)

urlpatterns = [
    url(
        regex=r'^(?P<pk>\d+)/$', view=KeyDetailView.as_view(),
        name='key_detail'
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$', view=KeyDeleteView.as_view(),
        name='key_delete'
    ),
    url(
        regex=r'^(?P<pk>\d+)/download/$', view=KeyDownloadView.as_view(),
        name='key_download'
    ),
    url(
        regex=r'^list/private/$', view=PrivateKeyListView.as_view(),
        name='key_private_list'
    ),
    url(
        regex=r'^list/public/$', view=PublicKeyListView.as_view(),
        name='key_public_list'
    ),
    url(
        regex=r'^upload/$', view=KeyUploadView.as_view(), name='key_upload'
    ),
    url(regex=r'^query/$', view=KeyQueryView.as_view(), name='key_query'),
    url(
        regex=r'^query/results/$', view=KeyQueryResultView.as_view(),
        name='key_query_results'
    ),
    url(
        regex=r'^receive/(?P<key_id>.+)/$', view=KeyReceive.as_view(),
        name='key_receive'
    ),
]

api_urls = [
    url(
        regex=r'^keys/(?P<pk>[0-9]+)/$', view=APIKeyView.as_view(),
        name='key-detail'
    ),
    url(regex=r'^keys/$', view=APIKeyListView.as_view(), name='key-list'),
]
