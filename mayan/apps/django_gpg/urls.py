from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    KeyDeleteView, KeyDetailView, KeyQueryView, KeyQueryResultView, KeyReceive,
    PrivateKeyListView, PublicKeyListView
)

urlpatterns = patterns(
    'django_gpg.views',
    url(
        r'^(?P<pk>\d+)/$', KeyDetailView.as_view(), name='key_detail'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$', KeyDeleteView.as_view(), name='key_delete'
    ),
    url(
        r'^list/private/$', PrivateKeyListView.as_view(),
        name='key_private_list'
    ),
    url(
        r'^list/public/$', PublicKeyListView.as_view(), name='key_public_list'
    ),
    url(r'^query/$', KeyQueryView.as_view(), name='key_query'),
    url(
        r'^query/results/$', KeyQueryResultView.as_view(),
        name='key_query_results'
    ),
    url(
        r'^receive/(?P<key_id>.+)/$', KeyReceive.as_view(), name='key_receive'
    ),
)
