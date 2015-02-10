from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from .views import APIBase, Version_0, APIAppView, BrowseableObtainAuthToken

version_0_urlpatterns = patterns('',
    url(r'^$', Version_0.as_view(), name='api-version-0'),
    url(r'^(?P<app_name>\w+)/$', APIAppView.as_view(), name='api-version-0-app'),
)

urlpatterns = patterns('',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v0/', include(version_0_urlpatterns)),
)

api_urls = patterns('',
    url(r'^auth/token/obtain/', BrowseableObtainAuthToken.as_view(), name='auth_token_obtain'),
)
