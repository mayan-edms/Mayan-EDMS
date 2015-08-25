from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics
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
from .serializers import (
    FolderDocumentSerializer, FolderSerializer, NewFolderDocumentSerializer,
    NewFolderSerializer
)


class APIDocumentFolderListView(generics.ListAPIView):
    """
    Returns a list of all the folders to which a document belongs.
    """

    serializer_class = FolderSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_folder_view,)}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user, document
            )

        queryset = document.document_folders().all()
        return queryset


class APIFolderListView(generics.ListCreateAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_folder_view,)}
    mayan_view_permissions = {'POST': (permission_folder_create,)}
    permission_classes = (MayanPermission,)
    queryset = Folder.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FolderSerializer
        elif self.request.method == 'POST':
            return NewFolderSerializer

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


class APIFolderView(generics.RetrieveUpdateDestroyAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_folder_view,),
        'PUT': (permission_folder_edit,),
        'PATCH': (permission_folder_edit,),
        'DELETE': (permission_folder_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

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


class APIFolderDocumentListView(generics.ListCreateAPIView):
    """
    Returns a list of all the documents contained in a particular folder.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_folder_view,),
        'POST': (permission_folder_add_document,)
    }

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FolderDocumentSerializer
        elif self.request.method == 'POST':
            return NewFolderDocumentSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'folder': self.get_folder(),
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }

    def get_folder(self):
        return get_object_or_404(Folder, pk=self.kwargs['pk'])

    def get_queryset(self):
        folder = self.get_folder()

        documents = folder.documents.all()

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            documents = AccessControlList.objects.filter_by_access(
                permission_document_view, self.request.user, documents
            )

        return documents

    def perform_create(self, serializer):
        serializer.save(folder=self.get_folder())

    def post(self, request, *args, **kwargs):
        """
        Add a document to the selected folder.
        """
        return super(APIFolderDocumentListView, self).post(request, *args, **kwargs)


class APIFolderDocumentView(generics.RetrieveDestroyAPIView):
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_folder_view,),
        'DELETE': (permission_folder_remove_document,)
    }
    serializer_class = FolderDocumentSerializer

    def delete(self, request, *args, **kwargs):
        """
        Remove a document from the selected folder.
        """

        return super(APIFolderDocumentView, self).delete(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Returns the details of the selected folder document.
        """

        return super(APIFolderDocumentView, self).get(*args, **kwargs)

    def get_folder(self):
        return get_object_or_404(Folder, pk=self.kwargs['folder_pk'])

    def get_queryset(self):
        return self.get_folder().documents.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'folder': self.get_folder(),
            'format': self.format_kwarg,
            'request': self.request,
            'view': self
        }

    def perform_destroy(self, instance):
        self.get_folder().documents.remove(instance)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user, instance
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
