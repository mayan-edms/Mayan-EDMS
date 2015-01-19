from __future__ import unicode_literals

import logging

from rest_framework import generics, renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .classes import APIEndPoint
from .serializers import APIAppSerializer, APISerializer, APIVersionSerializer

logger = logging.getLogger(__name__)

registered_version_0_endpoints = [
]


class APIBase(generics.GenericAPIView):
    """
    Main entry point of the API.
    """

    serializer_class = APISerializer

    def get(self, request, format=None):
        return Response([
            {'name': 'Version 0', 'url': reverse('api-version-0', request=request, format=format)}
        ])


class Version_0(generics.GenericAPIView):
    """
    API version 0 entry points.
    """

    serializer_class = APIVersionSerializer

    def get(self, request, format=None):
        return Response({
            'apps': [
                {'name': unicode(endpoint), 'url': reverse('api-version-0-app', args=[unicode(endpoint)], request=request, format=format)} for endpoint in APIEndPoint.get_all()
            ],
        })


class APIAppView(generics.GenericAPIView):
    """
    Entry points of the selected app.
    """

    serializer_class = APIAppSerializer

    def get(self, request, app_name, format=None):
        api_app = APIEndPoint.get(app_name)

        return Response({
            'name': api_app.name,
            'url': reverse('api-version-0-app', args=[unicode(api_app.name)], request=request, format=format)
        })


class BrowseableObtainAuthToken(ObtainAuthToken):
    """
    Obtain an API authentication token.
    """
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
