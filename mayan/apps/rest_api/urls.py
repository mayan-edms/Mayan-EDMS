from __future__ import unicode_literals

from django.conf.urls import include, patterns, url

from .views import APIBase, APIAppView, BrowseableObtainAuthToken


urlpatterns = patterns(
    '',
)

api_urls = patterns(
    '',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^api/(?P<path>.*)/?$', APIAppView.as_view(), name='api-app'),
    url(
        r'^auth/token/obtain/$', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
)
