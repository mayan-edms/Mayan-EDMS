from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_view, permission_document_type_edit
)
from mayan.apps.rest_api.filters import MayanObjectPermissionsFilter
from mayan.apps.rest_api.permissions import MayanPermission

from .models import MetadataType
from .permissions import (
    permission_document_metadata_add, permission_document_metadata_remove,
    permission_document_metadata_edit, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)
from .serializers import (
    DocumentMetadataSerializer, DocumentTypeMetadataTypeSerializer,
    MetadataTypeSerializer, NewDocumentMetadataSerializer,
    NewDocumentTypeMetadataTypeSerializer,
    WritableDocumentTypeMetadataTypeSerializer
)


class APIDocumentMetadataListView(generics.ListCreateAPIView):
    """
    get: Returns a list of selected document's metadata types and values.
    post: Add an existing metadata type and value to the selected document.
    """
    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_metadata_view
        else:
            permission_required = permission_document_metadata_add

        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_pk']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_required,),
            user=self.request.user
        )

        return document

    def get_queryset(self):
        return self.get_document().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentMetadataListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentMetadataSerializer
        else:
            return NewDocumentMetadataSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentMetadataListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context


class APIDocumentMetadataView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Remove this metadata entry from the selected document.
    get: Return the details of the selected document metadata type and value.
    patch: Edit the selected document metadata type and value.
    put: Edit the selected document metadata type and value.
    """
    lookup_url_kwarg = 'metadata_pk'

    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_metadata_view
        elif self.request.method == 'PUT':
            permission_required = permission_document_metadata_edit
        elif self.request.method == 'PATCH':
            permission_required = permission_document_metadata_edit
        elif self.request.method == 'DELETE':
            permission_required = permission_document_metadata_remove

        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_pk']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_required,),
            user=self.request.user
        )

        return document

    def get_queryset(self):
        return self.get_document().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentMetadataView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentMetadataSerializer
        else:
            return DocumentMetadataSerializer


class APIMetadataTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the metadata types.
    post: Create a new metadata type.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_metadata_type_view,)}
    mayan_view_permissions = {'POST': (permission_metadata_type_create,)}
    permission_classes = (MayanPermission,)
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypeSerializer


class APIMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected metadata type.
    get: Return the details of the selected metadata type.
    patch: Edit the selected metadata type.
    put: Edit the selected metadata type.
    """
    lookup_url_kwarg = 'metadata_type_pk'
    mayan_object_permissions = {
        'GET': (permission_metadata_type_view,),
        'PUT': (permission_metadata_type_edit,),
        'PATCH': (permission_metadata_type_edit,),
        'DELETE': (permission_metadata_type_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypeSerializer


class APIDocumentTypeMetadataTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of selected document type's metadata types.
    post: Add a metadata type to the selected document type.
    """
    lookup_url_kwarg = 'metadata_type_pk'

    def get_document_type(self):
        if self.request.method == 'GET':
            permission_required = permission_document_type_view
        else:
            permission_required = permission_document_type_edit

        document_type = get_object_or_404(
            klass=DocumentType, pk=self.kwargs['document_type_pk']
        )

        AccessControlList.objects.check_access(
            obj=document_type, permissions=(permission_required,),
            user=self.request.user
        )

        return document_type

    def get_queryset(self):
        return self.get_document_type().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTypeMetadataTypeListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeMetadataTypeSerializer
        else:
            return NewDocumentTypeMetadataTypeSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentTypeMetadataTypeListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document_type': self.get_document_type(),
                }
            )

        return context


class APIDocumentTypeMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Remove a metadata type from a document type.
    get: Retrieve the details of a document type metadata type.
    patch: Edit the selected document type metadata type.
    put: Edit the selected document type metadata type.
    """
    lookup_url_kwarg = 'metadata_type_pk'
    serializer_class = DocumentTypeMetadataTypeSerializer

    def get_document_type(self):
        if self.request.method == 'GET':
            permission_required = permission_document_type_view
        else:
            permission_required = permission_document_type_edit

        document_type = get_object_or_404(
            klass=DocumentType, pk=self.kwargs['document_type_pk']
        )

        AccessControlList.objects.check_access(
            obj=document_type, permissions=(permission_required,),
            user=self.request.user
        )

        return document_type

    def get_queryset(self):
        return self.get_document_type().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTypeMetadataTypeView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeMetadataTypeSerializer
        else:
            return WritableDocumentTypeMetadataTypeSerializer
