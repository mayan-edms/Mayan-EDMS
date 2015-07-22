from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_remove, permission_tag_view
)
from .serializers import TagSerializer


class APITagView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {'GET': [permission_tag_view]}

    def delete(self, *args, **kwargs):
        """Delete the selected tag."""
        return super(APITagView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected tag."""
        return super(APITagView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected tag."""
        return super(APITagView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected tag."""
        return super(APITagView, self).put(*args, **kwargs)


class APITagListView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_tag_view]}

    def get(self, *args, **kwargs):
        """Returns a list of all the tags."""
        return super(APITagListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new tag."""
        return super(APITagListView, self).post(*args, **kwargs)


class APITagDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents tagged by a particular tag.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_document_view]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, [permission_tag_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_tag_view, self.request.user, tag
            )

        queryset = tag.documents.all()
        return queryset


class APIDocumentTagListView(generics.ListAPIView):
    """
    Returns a list of all the tags attached to a document.
    """

    serializer_class = TagSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_tag_view]}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, [permission_document_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user, document
            )

        queryset = document.tags.all()
        return queryset


class APIDocumentTagView(views.APIView):
    def delete(self, request, *args, **kwargs):
        """
        Remove a tag from a document.
        """

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        try:
            Permission.check_permissions(request.user, [permission_tag_remove])
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_tag_remove, request.user, document
            )

        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        tag.documents.remove(document)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        """
        Attach a tag to a document.
        """

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        try:
            Permission.check_permissions(request.user, [permission_tag_attach])
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_tag_attach, request.user, document
            )

        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        tag.documents.add(document)
        return Response(status=status.HTTP_201_CREATED)
