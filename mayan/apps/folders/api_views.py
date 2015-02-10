from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from acls.models import AccessEntry
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Folder
from .permissions import (
    PERMISSION_FOLDER_ADD_DOCUMENT, PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_DELETE, PERMISSION_FOLDER_EDIT,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW
)
from .serializers import FolderSerializer


class APIFolderListView(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_FOLDER_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_FOLDER_CREATE]}

    def get(self, *args, **kwargs):
        """Returns a list of all the folders."""
        return super(APIFolderListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new folder."""
        return super(APIFolderListView, self).post(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.object.user = request.user
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIFolderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_FOLDER_VIEW],
        'PUT': [PERMISSION_FOLDER_EDIT],
        'PATCH': [PERMISSION_FOLDER_EDIT],
        'DELETE': [PERMISSION_FOLDER_DELETE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected folder."""
        return super(APIFolderView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Returns the details of the selected folder."""
        return super(APIFolderView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected folder."""
        return super(APIFolderView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected folder."""
        return super(APIFolderView, self).put(*args, **kwargs)


class APIFolderDocumentListView(generics.ListAPIView):
    """Returns a list of all the documents contained in a particular folder."""

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_FOLDER_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_FOLDER_VIEW, self.request.user, folder)

        return folder.documents.all()


class APIDocumentFolderListView(generics.ListAPIView):
    """Returns a list of all the folders to which a document belongs."""

    serializer_class = FolderSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_FOLDER_VIEW]}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, self.request.user, document)

        queryset = document.folders.all()
        return queryset


class APIFolderDocumentView(views.APIView):

    def delete(self, request, *args, **kwargs):
        """Remove a document from the selected folder."""

        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_REMOVE_DOCUMENT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_FOLDER_REMOVE_DOCUMENT, request.user, folder)

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        folder.documents.remove(document)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: move this method as post of APIFolderDocumentListView
    def post(self, request, *args, **kwargs):
        """Add a document to the selected folder."""

        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_ADD_DOCUMENT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_FOLDER_ADD_DOCUMENT, request.user, folder)

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        folder.documents.add(document)
        return Response(status=status.HTTP_201_CREATED)
