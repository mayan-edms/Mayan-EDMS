from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessEntry
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Folder
from .permissions import (PERMISSION_FOLDER_CREATE, PERMISSION_FOLDER_DELETE,
                          PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_VIEW)
from .serializers import FolderSerializer


class APIFolderListView(generics.ListCreateAPIView):
    """
    Returns a list of all the folders.
    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_FOLDER_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_FOLDER_CREATE]}


class APIFolderView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected folder details.
    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_FOLDER_VIEW],
        'PUT': [PERMISSION_FOLDER_EDIT],
        'PATCH': [PERMISSION_FOLDER_EDIT],
        'DELETE': [PERMISSION_FOLDER_DELETE]
    }


class APIFolderDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents contained in a particular folder.
    """

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

        queryset = folder.documents.all()
        return queryset


class APIDocumentFolderListView(generics.ListAPIView):
    """
    Returns a list of all the folders to which a document belongs.
    """

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
