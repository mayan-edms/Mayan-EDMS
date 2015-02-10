from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('statistics.views',
    url(r'^$', 'namespace_list', name='namespace_list'),
    url(r'^namespace/(?P<namespace_id>\w+)/details/$', 'namespace_details', name='namespace_details'),
    url(r'^(?P<statistic_id>\w+)/execute/$', 'execute', name='execute'),
)
