from __future__ import unicode_literals

from django.conf.urls import include, url

from .api_views import BrowseableObtainAuthToken


api_urls = [
    url(
        r'^auth/token/obtain/$', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
]

urlpatterns = [
    url(r'^', include(api_urls)),
]
