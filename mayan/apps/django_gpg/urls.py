from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import PrivateKeyListView, PublicKeyListView

urlpatterns = patterns(
    'django_gpg.views',
    url(
        r'^delete/(?P<fingerprint>.+)/(?P<key_type>\w+)/$', 'key_delete',
        name='key_delete'
    ),
    url(r'^list/private/$', PrivateKeyListView.as_view(), name='key_private_list'),
    url(r'^list/public/$', PublicKeyListView.as_view(), name='key_public_list'),
    url(r'^query/$', 'key_query', name='key_query'),
    url(r'^receive/(?P<key_id>.+)/$', 'key_receive', name='key_receive'),
)
