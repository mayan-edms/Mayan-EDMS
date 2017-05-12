from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APIResourceTypeListView
from .views import APIBase, BrowseableObtainAuthToken


urlpatterns = []

api_urls = [
    url(r'^$', APIBase.as_view(), name='api_root'),
    url(
        r'^resources/$', APIResourceTypeListView.as_view(),
        name='resource-list'
    ),
    url(
        r'^auth/token/obtain/$', BrowseableObtainAuthToken.as_view(),
        name='auth_token_obtain'
    ),
]
