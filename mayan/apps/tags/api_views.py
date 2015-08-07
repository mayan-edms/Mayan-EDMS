from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view
from documents.serializers import DocumentSerializer
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)
from .serializers import (
    DocumentTagSerializer, NewDocumentTagSerializer, TagSerializer
)


class APITagView(generics.RetrieveUpdateDestroyAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'DELETE': (permission_tag_delete,),
        'GET': (permission_tag_view,),
        'PATCH': (permission_tag_edit,),
        'PUT': (permission_tag_edit,)
    }
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def delete(self, *args, **kwargs):
        """
        Delete the selected tag.
        """

        return super(APITagView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Return the details of the selected tag.
        """

        return super(APITagView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the selected tag.
        """

        return super(APITagView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected tag.
        """

        return super(APITagView, self).put(*args, **kwargs)


class APITagListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_tag_view,)}
    mayan_view_permissions = {'POST': (permission_tag_create,)}
    permission_classes = (MayanPermission,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, *args, **kwargs):
        """
        Returns a list of all the tags.
        """

        return super(APITagListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new tag.
        """

        return super(APITagListView, self).post(*args, **kwargs)


class APITagDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents tagged by a particular tag.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, (permission_tag_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_tag_view, self.request.user, tag
            )

        return tag.documents.all()

###
class APIDocumentTagListView(generics.ListCreateAPIView):
    """
    Returns a list of all the tags attached to a document.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_tag_view,)}

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        document = self.get_document()
        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user, document
            )

        return document.tags.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTagSerializer
        elif self.request.method == 'POST':
            return NewDocumentTagSerializer

    def perform_create(self, serializer):
        serializer.save(document=self.get_document())

    def post(self, request, *args, **kwargs):
        """
        Attach a tag to a document.
        """

        return super(APIDocumentTagListView, self).post(request, *args, **kwargs)


class APIDocumentTagView(generics.RetrieveDestroyAPIView):
    serialize_class = DocumentTagSerializer

    def get_folder(self):
        return get_object_or_404(Document, pk=self.kwargs['document_pk'])

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'document': self.get_document(),
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }

    '''
    def delete(self, request, *args, **kwargs):
        """
        Remove a tag from a document.
        """

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])

        try:
            Permission.check_permissions(request.user, (permission_tag_remove,))
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_tag_remove, request.user, document
            )

        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        tag.documents.remove(document)
        return Response(status=status.HTTP_204_NO_CONTENT)

    '''
