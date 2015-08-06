from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from .views import APIBase, APIVersionView, APIAppView, BrowseableObtainAuthToken

version_1_urlpatterns = patterns(
    '',
    url(r'^$', APIVersionView.as_view(), name='api-version-1'),
    url(
        r'^(?P<app_name>\w+)/$', APIAppView.as_view(),
        name='api-version-1-app'
    ),
)

urlpatterns = patterns(
    '',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v1/', include(version_1_urlpatterns)),
)

api_urls = patterns(
    '',
    url(
        r'^auth/token/obtain/', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
)
