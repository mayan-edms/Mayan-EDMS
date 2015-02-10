from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from acls.models import AccessEntry
from documents.models import Document, DocumentType
from documents.permissions import (
    PERMISSION_DOCUMENT_TYPE_VIEW, PERMISSION_DOCUMENT_TYPE_EDIT
)
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import DocumentMetadata, MetadataType
from .permissions import (
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_EDIT, PERMISSION_METADATA_DOCUMENT_VIEW,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_EDIT, PERMISSION_METADATA_TYPE_VIEW
)
from .serializers import (
    DocumentMetadataSerializer, DocumentTypeNewMetadataTypeSerializer,
    MetadataTypeSerializer, DocumentTypeMetadataTypeSerializer
)


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


class APIDocumentMetadataListView(generics.ListCreateAPIView):
    permission_classes = (MayanPermission,)
    serializer_class = DocumentMetadataSerializer

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['document_pk'])

    def get_queryset(self):
        document = self.get_document()

        if self.request == 'GET':
            # Make sure the use has the permission to see the metadata for this document
            try:
                Permission.objects.check_permissions(self.request.user, [PERMISSION_METADATA_DOCUMENT_VIEW])
            except PermissionDenied:
                AccessEntry.objects.check_access(PERMISSION_METADATA_DOCUMENT_VIEW, self.request.user, document)
            else:
                return document.metadata.all()
        elif self.request == 'POST':
            # Make sure the use has the permission to add metadata to this document
            try:
                Permission.objects.check_permissions(self.request.user, [PERMISSION_METADATA_DOCUMENT_ADD])
            except PermissionDenied:
                AccessEntry.objects.check_access(PERMISSION_METADATA_DOCUMENT_ADD, self.request.user, document)
            else:
                return document.metadata.all()

    def pre_save(self, serializer):
        serializer.document = self.get_document()

    def get(self, *args, **kwargs):
        """Returns a list of selected document's metadata types and values."""
        return super(APIDocumentMetadataListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Add an existing metadata type and value to the selected document."""
        return super(APIDocumentMetadataListView, self).post(*args, **kwargs)


class APIDocumentMetadataView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentMetadataSerializer
    queryset = DocumentMetadata.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_METADATA_DOCUMENT_VIEW],
        'PUT': [PERMISSION_METADATA_DOCUMENT_EDIT],
        'PATCH': [PERMISSION_METADATA_DOCUMENT_EDIT],
        'DELETE': [PERMISSION_METADATA_DOCUMENT_REMOVE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected document metadata type and value."""
        try:
            return super(APIDocumentMetadataView, self).delete(*args, **kwargs)
        except Exception as exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'non_fields_errors': unicode(exception)})

    def get(self, *args, **kwargs):
        """Return the details of the selected document metadata type and value."""
        return super(APIDocumentMetadataView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Edit the selected document metadata type and value."""
        try:
            return super(APIDocumentMetadataView, self).patch(*args, **kwargs)
        except Exception as exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'non_fields_errors': unicode(exception)})

    def put(self, *args, **kwargs):
        """Edit the selected document metadata type and value."""
        try:
            return super(APIDocumentMetadataView, self).put(*args, **kwargs)
        except Exception as exception:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'non_fields_errors': unicode(exception)})


class APIDocumentTypeMetadataTypeOptionalListView(generics.ListCreateAPIView):
    permission_classes = (MayanPermission,)

    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_TYPE_EDIT]}

    required_metadata = False

    def get_queryset(self):
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['document_type_pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_VIEW, self.request.user, document_type)

        return document_type.metadata.filter(required=self.required_metadata)

    def get(self, *args, **kwargs):
        """Returns a list of selected document type's optional metadata types."""
        return super(APIDocumentTypeMetadataTypeOptionalListView, self).get(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeMetadataTypeSerializer
        elif self.request.method == 'POST':
            return DocumentTypeNewMetadataTypeSerializer

    def post(self, request, *args, **kwargs):
        """
        Add an optional metadata type to a document type.
        """
        document_type = get_object_or_404(DocumentType, pk=self.kwargs['document_type_pk'])

        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_TYPE_EDIT, self.request.user, document_type)

        serializer = self.get_serializer(data=self.request.POST)

        if serializer.is_valid():
            metadata_type = get_object_or_404(MetadataType, pk=serializer.data['metadata_type_pk'])
            document_type.metadata_type.add(metadata_type, required=self.required_metadata)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class APIDocumentTypeMetadataTypeRequiredListView(APIDocumentTypeMetadataTypeOptionalListView):
    required_metadata = True

    def get(self, *args, **kwargs):
        """Returns a list of the selected document type's required metadata types."""
        return super(APIDocumentTypeMetadataTypeRequiredListView, self).get(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Add a required metadata type to a document type.
        """
        return super(APIDocumentTypeMetadataTypeRequiredListView, self).get(*args, **kwargs)


class APIDocumentTypeMetadataTypeRequiredView(views.APIView):
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
        document_type.metadata_type.remove(metadata_type)
        return Response(status=status.HTTP_204_NO_CONTENT)
