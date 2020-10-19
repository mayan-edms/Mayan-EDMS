import logging

from mayan.apps.rest_api import generics

from ..models.document_type_models import DocumentType
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
    permission_document_view
)
from ..serializers.document_serializers import DocumentSerializer
from ..serializers.document_type_serializers import (
    DocumentTypeSerializer, DocumentTypeWritableSerializer
)

from .mixins import ParentObjectDocumentTypeAPIViewMixin

logger = logging.getLogger(name=__name__)


class APIDocumentTypeListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the document types.
    post: Create a new document type.
    """
    mayan_object_permissions = {'GET': (permission_document_type_view,)}
    mayan_view_permissions = {'POST': (permission_document_type_create,)}
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeSerializer
        else:
            return DocumentTypeWritableSerializer


class APIDocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected document type.
    get: Return the details of the selected document type.
    patch: Edit the properties of the selected document type.
    put: Edit the properties of the selected document type.
    """
    lookup_url_kwarg = 'document_type_id'
    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
        'PUT': (permission_document_type_edit,),
        'PATCH': (permission_document_type_edit,),
        'DELETE': (permission_document_type_delete,)
    }
    queryset = DocumentType.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTypeSerializer
        else:
            return DocumentTypeWritableSerializer


class APIDocumentTypeDocumentListView(
    ParentObjectDocumentTypeAPIViewMixin, generics.ListAPIView
):
    """
    Returns a list of all the documents of a particular document type.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return self.get_document_type(
            permission=permission_document_type_view
        ).documents.all()
