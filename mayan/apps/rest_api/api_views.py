from __future__ import unicode_literals

from drf_yasg.views import get_schema_view

from rest_framework import permissions, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas.generators import EndpointEnumerator

from .classes import Endpoint
from .serializers import EndpointSerializer
from .schemas import openapi_info


class APIRoot(APIView):
    swagger_schema = None

    def get(self, request, format=None):
        """
        get: Return a list of all endpoints.
        """
        endpoint_enumerator = EndpointEnumerator()

        endpoints = []
        for url in sorted(set([entry[0].split('/')[2] for entry in endpoint_enumerator.get_api_endpoints()])):
            if url:
                endpoints.append(Endpoint(label=url))

        serializer = EndpointSerializer(endpoints, many=True)
        return Response(serializer.data)


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
