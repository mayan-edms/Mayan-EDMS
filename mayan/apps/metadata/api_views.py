from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics

from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import DocumentMetadata, MetadataType
from .permissions import (PERMISSION_METADATA_DOCUMENT_ADD,
                          PERMISSION_METADATA_DOCUMENT_REMOVE,
                          PERMISSION_METADATA_DOCUMENT_EDIT,
                          PERMISSION_METADATA_DOCUMENT_VIEW,
                          PERMISSION_METADATA_TYPE_CREATE,
                          PERMISSION_METADATA_TYPE_DELETE,
                          PERMISSION_METADATA_TYPE_EDIT,
                          PERMISSION_METADATA_TYPE_VIEW)
from .serializers import DocumentMetadataSerializer, MetadataTypeSerializer


class APIMetadataTypeListView(generics.ListCreateAPIView):
    """
    Returns a list of all the metadata type.
    """

    serializer_class = MetadataTypeSerializer
    queryset = MetadataType.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_METADATA_TYPE_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_METADATA_TYPE_CREATE]}


class APIMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected metadata type details.
    """

    serializer_class = MetadataTypeSerializer
    queryset = MetadataType.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_METADATA_TYPE_VIEW],
        'PUT': [PERMISSION_METADATA_TYPE_EDIT],
        'PATCH': [PERMISSION_METADATA_TYPE_EDIT],
        'DELETE': [PERMISSION_METADATA_TYPE_DELETE]
    }


class APIDocumentMetadataListView(generics.ListCreateAPIView):
    """
    Returns a list of all the metadata of a document.
    """

    serializer_class = DocumentMetadataSerializer
    permission_classes = (MayanPermission,)

    mayan_view_permissions = {'POST': [PERMISSION_METADATA_DOCUMENT_ADD]}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_METADATA_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_METADATA_DOCUMENT_VIEW, self.request.user, document)

        queryset = document.metadata.all()
        return queryset


class APIDocumentMetadataView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document metadata details.
    """

    serializer_class = DocumentMetadataSerializer
    queryset = DocumentMetadata.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_METADATA_DOCUMENT_VIEW],
        'PUT': [PERMISSION_METADATA_DOCUMENT_EDIT],
        'PATCH': [PERMISSION_METADATA_DOCUMENT_EDIT],
        'DELETE': [PERMISSION_METADATA_DOCUMENT_REMOVE]
    }
