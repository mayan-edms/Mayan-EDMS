from __future__ import absolute_import

from django.conf.urls import include, patterns, url

#from .classes import EndPoint
from .views import APIBase, Version_0, EndPointView

version_0_endpoints_urlpatterns = patterns('',
    url(r'^$', Version_0.as_view(), name='api-version-0'),
    url(r'^(?P<endpoint_name>\w+)$', EndPointView.as_view(), name='api-version-0-endpoint'),
)

"""
for endpoint in EndPoint.get_all():
    endpoint_urlpatterns = patterns('')

    for service in endpoint.services:
        endpoint_urlpatterns += patterns('', service['urlpattern'])

    version_0_endpoints_urlpatterns += patterns('', url(r'^%s/' % endpoint.name, include(endpoint_urlpatterns)))
"""

urlpatterns = patterns('',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v0/', include(version_0_endpoints_urlpatterns)),
)
