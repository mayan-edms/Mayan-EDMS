from django.conf.urls import url

from .api_views import APIKeyListView, APIKeyView
from .views import (
    KeyDeleteView, KeyDetailView, KeyDownloadView, KeyQueryView,
    KeyQueryResultView, KeyReceive, KeyUploadView, PrivateKeyListView,
    PublicKeyListView
)

urlpatterns = [
    url(
        regex=r'^keys/(?P<key_id>\d+)/$', name='key_detail',
        view=KeyDetailView.as_view()
    ),
    url(
        regex=r'^keys/(?P<key_id>\d+)/delete/$', name='key_delete',
        view=KeyDeleteView.as_view()
    ),
    url(
        regex=r'^keys/(?P<key_id>\d+)/download/$', name='key_download',
        view=KeyDownloadView.as_view()
    ),
    url(
        regex=r'^keys/private/$', name='key_private_list',
        view=PrivateKeyListView.as_view()
    ),
    url(
        regex=r'^keys/public/$', name='key_public_list',
        view=PublicKeyListView.as_view()
    ),
    url(
        regex=r'^keys/upload/$', name='key_upload',
        view=KeyUploadView.as_view()
    ),
    url(
        regex=r'^keys/query/$', name='key_query', view=KeyQueryView.as_view()
    ),
    url(
        regex=r'^keys/query/results/$', name='key_query_results',
        view=KeyQueryResultView.as_view()
    ),
    # Key ID for this view is not the key's DB ID by the embedded
    # alphanumeric ID.
    url(
        regex=r'^keys/receive/(?P<key_id>.+)/$', name='key_receive',
        view=KeyReceive.as_view()
    )
]

api_urls = [
    url(
        regex=r'^keys/(?P<pk>[0-9]+)/$', name='key-detail',
        view=APIKeyView.as_view()
    ),
    url(regex=r'^keys/$', name='key-list', view=APIKeyListView.as_view())
]
