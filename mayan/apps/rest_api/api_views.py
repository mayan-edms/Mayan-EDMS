from __future__ import unicode_literals

from rest_framework import renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas.generators import EndpointEnumerator

from .classes import Endpoint
from .serializers import EndpointSerializer


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
