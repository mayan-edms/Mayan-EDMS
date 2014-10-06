from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
from taggit.models import Tag

from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .permissions import PERMISSION_TAG_VIEW
from .serializers import TagSerializer


class APITagView(generics.RetrieveAPIView):
    """
    Details of the selected tag.
    """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {'GET': [PERMISSION_TAG_VIEW]}


class APITagListView(generics.ListAPIView):
    """
    Returns a list of all the tags.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_TAG_VIEW]}


class APITagDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents tagged by a particular tag.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_TAG_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_TAG_VIEW, self.request.user, tag)

        queryset = tag.documents.all()
        return queryset


class APIDocumentTagListView(generics.ListAPIView):
    """
    Returns a list of all the tags attached to a document.
    """

    serializer_class = TagSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_TAG_VIEW]}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, self.request.user, document)

        queryset = document.tags.all()
        return queryset
