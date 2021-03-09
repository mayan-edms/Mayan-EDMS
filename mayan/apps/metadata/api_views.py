from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_view, permission_document_type_edit
)
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import MetadataType
from .permissions import (
    permission_document_metadata_add, permission_document_metadata_remove,
    permission_document_metadata_edit, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)
from .serializers import (
    DocumentMetadataSerializer, DocumentTypeMetadataTypeSerializer,
    MetadataTypeSerializer, NewDocumentTypeMetadataTypeSerializer,
    WritableDocumentTypeMetadataTypeSerializer
)


class APIDocumentMetadataListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of selected document's metadata types and values.
    post: Add an existing metadata type and value to the selected document.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permissions = {
        'GET': (permission_document_metadata_view,),
        'POST': (permission_document_metadata_add,)
    }
    mayan_object_permissions = {
        'GET': (permission_document_metadata_view,)
    }
    ordering_fields = ('metadata_type', 'value')
    serializer_class = DocumentMetadataSerializer

    def get_queryset(self):
        return self.external_object.metadata.all()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.external_object
        }

    def perform_create(self, serializer):
        if 'metadata_type_id' in serializer.validated_data:
            serializer.validated_data['metadata_type'] = serializer.validated_data['metadata_type_id']

        return super().perform_create(serializer=serializer)


class APIDocumentMetadataView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Remove this metadata entry from the selected document.
    get: Return the details of the selected document metadata type and value.
    patch: Edit the selected document metadata type and value.
    put: Edit the selected document metadata type and value.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    lookup_url_kwarg = 'metadata_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_document_metadata_remove,),
        'GET': (permission_document_metadata_view,),
        'PATCH': (permission_document_metadata_edit,),
        'PUT': (permission_document_metadata_edit,)
    }
    mayan_object_permissions = {
        'DELETE': (permission_document_metadata_remove,),
        'GET': (permission_document_metadata_view,),
        'PATCH': (permission_document_metadata_edit,),
        'PUT': (permission_document_metadata_edit,)
    }
    serializer_class = DocumentMetadataSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.external_object.metadata.all()


class APIMetadataTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the metadata types.
    post: Create a new metadata type.
    """
    mayan_object_permissions = {'GET': (permission_metadata_type_view,)}
    mayan_view_permissions = {'POST': (permission_metadata_type_create,)}
    ordering_fields = ('label', 'name')
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIMetadataTypeView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected metadata type.
    get: Return the details of the selected metadata type.
    patch: Edit the selected metadata type.
    put: Edit the selected metadata type.
    """
    lookup_url_kwarg = 'metadata_type_id'
    mayan_object_permissions = {
        'GET': (permission_metadata_type_view,),
        'PUT': (permission_metadata_type_edit,),
        'PATCH': (permission_metadata_type_edit,),
        'DELETE': (permission_metadata_type_delete,)
    }
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentTypeMetadataTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of selected document type's metadata types.
    post: Add a metadata type to the selected document type.
    """
    lookup_url_kwarg = 'metadata_type_id'

    def get_document_type(self):
        if self.request.method == 'GET':
            permission_required = permission_document_type_view
        else:
            permission_required = permission_document_type_edit

        document_type = get_object_or_404(
            klass=DocumentType, pk=self.kwargs['document_type_id']
        )

        AccessControlList.objects.check_access(
            obj=document_type, permissions=(permission_required,),
            user=self.request.user
        )

        return document_type

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.get_document_type().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeMetadataTypeSerializer
        else:
            return NewDocumentTypeMetadataTypeSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
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
    lookup_url_kwarg = 'metadata_type_id'
    serializer_class = DocumentTypeMetadataTypeSerializer

    def get_document_type(self):
        if self.request.method == 'GET':
            permission_required = permission_document_type_view
        else:
            permission_required = permission_document_type_edit

        document_type = get_object_or_404(
            klass=DocumentType, pk=self.kwargs['document_type_id']
        )

        AccessControlList.objects.check_access(
            obj=document_type, permissions=(permission_required,),
            user=self.request.user
        )

        return document_type

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.get_document_type().metadata.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeMetadataTypeSerializer
        else:
            return WritableDocumentTypeMetadataTypeSerializer
