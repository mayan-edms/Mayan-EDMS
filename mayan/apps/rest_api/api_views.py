from __future__ import unicode_literals

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .classes import APIResource
from .serializers import APIResourceSerializer


class APIResourceTypeListView(generics.ListAPIView):
    """
    Returns a list of all the available API resources.
    """

    serializer_class = APIResourceSerializer
    def get_queryset(self):
        return APIResource.all()
