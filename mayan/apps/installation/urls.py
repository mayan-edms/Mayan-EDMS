from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'installation.views',
    url(r'^$', 'namespace_list', name='namespace_list'),
    url(
        r'^(?P<namespace_id>\w+)/details/$', 'namespace_details',
        name='namespace_details'
    ),
)
