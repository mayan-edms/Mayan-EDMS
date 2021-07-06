import logging

from mayan.apps.rest_api import generics

from ..models.document_type_models import DocumentType
from ..permissions import (
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view
)
from ..serializers.document_type_serializers import (
    DocumentTypeQuickLabelSerializer, DocumentTypeSerializer,
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
    ordering_fields = ('id', 'label')
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected document type.
    get: Return the details of the selected document type.
    patch: Edit the properties of the selected document type.
    put: Edit the properties of the selected document type.
    """
    lookup_url_kwarg = 'document_type_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_type_delete,),
        'GET': (permission_document_type_view,),
        'PATCH': (permission_document_type_edit,),
        'PUT': (permission_document_type_edit,)
    }
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentTypeQuickLabelDetailView(
    ParentObjectDocumentTypeAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected quick label.
    get: Return the details of the selected quick label.
    patch: Edit the properties of the selected quick label.
    put: Edit the properties of the selected quick label.
    """
    lookup_url_kwarg = 'document_type_quick_label_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_type_edit,),
        'GET': (permission_document_type_view,),
        'PATCH': (permission_document_type_edit,),
        'PUT': (permission_document_type_edit,)
    }
    ordering_fields = ('filename', 'enabled', 'id')
    serializer_class = DocumentTypeQuickLabelSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.get_document_type().filenames.all()


class APIDocumentTypeQuickLabelListView(
    ParentObjectDocumentTypeAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the document type quick labels.
    post: Create a new document type quick label.
    """
    serializer_class = DocumentTypeQuickLabelSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'document_type': self.get_document_type(
                permission=permission_document_type_edit
            )
        }

    def get_queryset(self):
        # This method is only called during GET, therefore filter only by
        # the view permission.
        return self.get_document_type(
            permission=permission_document_type_view
        ).filenames.all()
