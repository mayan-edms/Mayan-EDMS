from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_gpg.views',
    url(r'^delete/(?P<fingerprint>.+)/(?P<key_type>\w+)/$', 'key_delete', (), 'key_delete'),
    url(r'^list/private/$', 'key_list', {'secret': True}, 'key_private_list'),
    url(r'^list/public/$', 'key_list', {'secret': False}, 'key_public_list'),
    url(r'^query/$', 'key_query', (), 'key_query'),
    url(r'^receive/(?P<key_id>.+)/$', 'key_receive', (), 'key_receive'),
)
