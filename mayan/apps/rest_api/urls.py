from __future__ import unicode_literals

from django.conf.urls import include, url

from .api_views import APIRoot, BrowseableObtainAuthToken


api_urls = [
    # FIXME: Defining a root API path confuses Swagger which then
    # groups all endpoints into a single dropdown. Disable until a
    # workaround is found for Swagger.

    # url(r'^$', APIRoot.as_view(), name='api_root'),
    url(
        r'^auth/token/obtain/$', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
]

urlpatterns = [
    url(r'^', include(api_urls)),
]
