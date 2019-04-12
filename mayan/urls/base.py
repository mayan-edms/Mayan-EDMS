from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib import admin

from drf_yasg.views import get_schema_view
from rest_framework import permissions

from mayan.apps.rest_api.schemas import openapi_info

__all__ = ('urlpatterns',)

admin.autodiscover()
schema_view = get_schema_view(
    openapi_info,
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]
