from __future__ import unicode_literals

import logging

from rest_framework import generics, renderers
from rest_framework.authtoken.views import ObtainAuthToken

from .classes import APIVersion, APIEndPoint
from .serializers import APIAppSerializer, APIVersionSerializer

logger = logging.getLogger(__name__)

registered_version_1_endpoints = [
]


class APIBase(generics.RetrieveAPIView):
    """
    Main entry point of the API.
    """

    serializer_class = APIVersionSerializer

    def get_object(self):
        return APIVersion()


class APIVersionView(generics.ListAPIView):
    """
    API version entry points.
    """

    serializer_class = APIAppSerializer

    def get_queryset(self):
        return APIEndPoint.get_all()


class APIAppView(generics.RetrieveAPIView):
    """
    Entry points of the selected app.
    """

    serializer_class = APIAppSerializer

    def get_object(self):
        return APIEndPoint.get(self.kwargs['app_name'])


class BrowseableObtainAuthToken(ObtainAuthToken):
    """
    Obtain an API authentication token.
    """
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)
