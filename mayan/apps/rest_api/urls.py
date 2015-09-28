from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import APIBase, APIAppView, BrowseableObtainAuthToken


urlpatterns = patterns(
    '',
)

api_urls = patterns(
    '',
    url(r'^$', APIBase.as_view(), name='api_root'),
    url(r'^api/(?P<path>.*)/?$', APIAppView.as_view(), name='api_app'),
    url(
        r'^auth/token/obtain/$', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
)
