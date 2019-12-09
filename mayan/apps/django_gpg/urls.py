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
        regex=r'^keys/(?P<pk>\d+)/$', view=KeyDetailView.as_view(),
        name='key_detail'
    ),
    url(
        regex=r'^keys/(?P<pk>\d+)/delete/$', view=KeyDeleteView.as_view(),
        name='key_delete'
    ),
    url(
        regex=r'^keys/(?P<pk>\d+)/download/$', view=KeyDownloadView.as_view(),
        name='key_download'
    ),
    url(
        regex=r'^keys/private/$', view=PrivateKeyListView.as_view(),
        name='key_private_list'
    ),
    url(
        regex=r'^keys/public/$', view=PublicKeyListView.as_view(),
        name='key_public_list'
    ),
    url(
        regex=r'^keys/upload/$', view=KeyUploadView.as_view(), name='key_upload'
    ),
    url(regex=r'^keys/query/$', view=KeyQueryView.as_view(), name='key_query'),
    url(
        regex=r'^keys/query/results/$', view=KeyQueryResultView.as_view(),
        name='key_query_results'
    ),
    url(
        regex=r'^keys/receive/(?P<key_id>.+)/$', view=KeyReceive.as_view(),
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
