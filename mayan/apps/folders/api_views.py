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

from .models import Folder
from .permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit,
    permission_folder_remove_document, permission_folder_view
)
from .serializers import FolderSerializer


class APIFolderListView(generics.ListCreateAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_folder_view]}
    mayan_view_permissions = {'POST': [permission_folder_create]}

    def get(self, *args, **kwargs):
        """
        Returns a list of all the folders.
        """
        return super(APIFolderListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Create a new folder.
        """
        return super(APIFolderListView, self).post(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.DATA, files=request.FILES
        )

        if serializer.is_valid():
            serializer.object.user = request.user
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIFolderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [permission_folder_view],
        'PUT': [permission_folder_edit],
        'PATCH': [permission_folder_edit],
        'DELETE': [permission_folder_delete]
    }

    def delete(self, *args, **kwargs):
        """
        Delete the selected folder.
        """
        return super(APIFolderView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Returns the details of the selected folder.
        """
        return super(APIFolderView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        Edit the selected folder.
        """
        return super(APIFolderView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Edit the selected folder.
        """
        return super(APIFolderView, self).put(*args, **kwargs)


class APIFolderDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents contained in a particular folder.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_document_view]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, [permission_folder_view]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_folder_view, self.request.user, folder
            )

        return folder.documents.all()


class APIDocumentFolderListView(generics.ListAPIView):
    """
    Returns a list of all the folders to which a document belongs.
    """

    serializer_class = FolderSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [permission_folder_view]}

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

        queryset = document.folders.all()
        return queryset


class APIFolderDocumentView(views.APIView):

    def delete(self, request, *args, **kwargs):
        """
        Remove a document from the selected folder.
        """

        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                request.user, [permission_folder_remove_document]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_folder_remove_document, request.user, folder
            )

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        folder.documents.remove(document)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: move this method as post of APIFolderDocumentListView
    def post(self, request, *args, **kwargs):
        """
        Add a document to the selected folder.
        """

        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                request.user, [permission_folder_add_document]
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_folder_add_document, request.user, folder
            )

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        folder.documents.add(document)
        return Response(status=status.HTTP_201_CREATED)
