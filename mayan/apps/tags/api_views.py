from __future__ import absolute_import

from rest_framework import generics

from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import PERMISSION_TAG_VIEW
from taggit.models import Tag
from .serializers import TagSerializer


class APITagView(generics.RetrieveAPIView):
    """
    Details of the selected tag.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = [PERMISSION_TAG_VIEW]


class APITagListView(generics.ListAPIView):
    """
    Returns a list of all the tags.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = [PERMISSION_TAG_VIEW]
