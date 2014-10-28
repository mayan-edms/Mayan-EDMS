from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from acls.models import AccessEntry
from documents.models import Document, DocumentType
from documents.permissions import (PERMISSION_DOCUMENT_TYPE_VIEW,
                                   PERMISSION_DOCUMENT_TYPE_EDIT)

from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import DocumentMetadata, MetadataType
from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
                          PERMISSION_METADATA_DOCUMENT_VIEW,
                          PERMISSION_METADATA_TYPE_CREATE,
                          PERMISSION_METADATA_TYPE_DELETE,
                          PERMISSION_METADATA_TYPE_EDIT,
                          PERMISSION_METADATA_TYPE_VIEW)
from .serializers import DocumentMetadataSerializer, MetadataTypeSerializer


class APIMetadataTypeListView(generics.ListCreateAPIView):
    serializer_class = MetadataTypeSerializer
    queryset = MetadataType.objects.all()

    permission_classes = (MayanPermission,)
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_METADATA_TYPE_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_METADATA_TYPE_CREATE]}

    def get(self, *args, **kwargs):
        """Returns a list of all the metadata types."""
        return super(APIMetadataTypeListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new metadata type."""
        return super(APIMetadataTypeListView, self).post(*args, **kwargs)


class APIMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MetadataTypeSerializer
    queryset = MetadataType.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_METADATA_TYPE_VIEW],
        'PUT': [PERMISSION_METADATA_TYPE_EDIT],
        'PATCH': [PERMISSION_METADATA_TYPE_EDIT],
        'DELETE': [PERMISSION_METADATA_TYPE_DELETE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected metadata type."""
        return super(APIMetadataTypeView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Return the details of the selected metadata type."""
        return super(APIMetadataTypeView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected metadata type."""
        return super(APIMetadataTypeView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected metadata type."""
        return super(APIMetadataTypeView, self).put(*args, **kwargs)


class APIDocumentMetadataListView(generics.ListAPIView):
    serializer_class = DocumentMetadataSerializer

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_METADATA_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_METADATA_DOCUMENT_VIEW, self.request.user, document)

        queryset = document.metadata.all()
        return queryset

    def get(self, *args, **kwargs):
        """Returns a list of selected document's metadata types and values."""
        return super(APIDocumentMetadataListView, self).get(*args, **kwargs)


class APIDocumentMetadataView(generics.RetrieveUpdateAPIView):
    serializer_class = DocumentMetadataSerializer
    queryset = DocumentMetadata.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_METADATA_DOCUMENT_VIEW],
        'PUT': [PERMISSION_METADATA_DOCUMENT_EDIT],
        'PATCH': [PERMISSION_METADATA_DOCUMENT_EDIT],
    }

    def get(self, *args, **kwargs):
        """Return the details of the selected document metadata type and value."""
        return super(APIDocumentMetadataView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected document metadata type and value."""
        return super(APIDocumentMetadataView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit the selected document metadata type and value."""
        return super(APIDocumentMetadataView, self).put(*args, **kwargs)


class APIDocumentTypeMetadataTypeListView(generics.ListAPIView):
    serializer_class = MetadataTypeSerializer
    permission_classes = (MayanPermission,)

    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_TYPE_EDIT]}

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['document_type_pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_VIEW, self.request.user, document_type)

        return document_type.metadata.all()

    def get(self, *args, **kwargs):
        """Returns a list of selected document type allowed metadata types."""
        return super(APIDocumentTypeMetadataTypeListView, self).get(*args, **kwargs)


class APIDocumentTypeMetadataTypeView(views.APIView):
    def delete(self, request, *args, **kwargs):
        """
        Remove a metadata type from a document type.
        """

        document_type = get_object_or_404(DocumentType, pk=self.kwargs['document_type_pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_EDIT, self.request.user, document_type)

        metadata_type = get_object_or_404(MetadataType, pk=self.kwargs['metadata_type_pk'])
        document_type.metadata.remove(metadata_type)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        """
        Add a metadata type to a document type.
        """

        document_type = get_object_or_404(DocumentType, pk=self.kwargs['document_type_pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_EDIT, self.request.user, document_type)

        metadata_type = get_object_or_404(MetadataType, pk=self.kwargs['metadata_type_pk'])
        document_type.metadata.add(metadata_type)
        return Response(status=status.HTTP_201_CREATED)
