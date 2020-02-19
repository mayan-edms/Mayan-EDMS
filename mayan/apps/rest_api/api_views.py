from __future__ import unicode_literals

from drf_yasg.views import get_schema_view

from rest_framework import permissions, renderers
from rest_framework.authtoken.views import ObtainAuthToken

from .schemas import openapi_info


class BrowseableObtainAuthToken(ObtainAuthToken):
    """
    Obtain an API authentication token.
    """
    renderer_classes = (renderers.BrowsableAPIRenderer, renderers.JSONRenderer)


schema_view = get_schema_view(
    openapi_info,
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
