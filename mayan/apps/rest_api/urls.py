from django.conf.urls import include, url

from .api_views import (
    APIRoot, APIVersionRoot, BrowseableObtainAuthToken,
    ProjectInformationAPIView, schema_view
)
from .literals import API_VERSION


api_version_urls = [
    url(regex=r'^$', name='api_version_root', view=APIVersionRoot.as_view()),
    url(
        regex=r'^auth/token/obtain/$', name='auth_token_obtain',
        view=BrowseableObtainAuthToken.as_view()
    ),
    url(
        regex=r'^project/$', name='project_information',
        view=ProjectInformationAPIView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^swagger(?P<format>.json|.yaml)$', name='schema-json',
        view=schema_view.without_ui(cache_timeout=None),
    ),
    url(regex=r'^v{}/'.format(API_VERSION), view=include(api_version_urls)),
    url(regex=r'^$', name='api_root', view=APIRoot.as_view()),
]

urlpatterns = [
    url(
        regex=r'^swagger/ui/$', name='schema-swagger-ui',
        view=schema_view.with_ui('swagger', cache_timeout=None)
    ),
    url(
        regex=r'^redoc/ui/$', name='schema-redoc',
        view=schema_view.with_ui('redoc', cache_timeout=None)
    ),
    url(regex=r'^', view=include(api_urls)),
]
