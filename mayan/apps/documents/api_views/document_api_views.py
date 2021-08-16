import logging

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api import generics

from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..permissions import (
    permission_document_create, permission_document_properties_edit,
    permission_document_trash, permission_document_view
)
from ..serializers.document_serializers import (
    DocumentSerializer, DocumentChangeTypeSerializer,
    DocumentUploadSerializer
)

logger = logging.getLogger(name=__name__)


class APIDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns the selected document details.
    delete: Move the selected document to the thrash.
    get: Return the details of the selected document.
    patch: Edit the properties of the selected document.
    put: Edit the properties of the selected document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'GET': (permission_document_view,),
        'PUT': (permission_document_properties_edit,),
        'PATCH': (permission_document_properties_edit,),
        'DELETE': (permission_document_trash,)
    }
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the documents.
    post: Create a new document.
    """
    mayan_object_permissions = {
        'GET': (permission_document_view,),
    }
    ordering_fields = ('datetime_created', 'document_type', 'id', 'label')
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        queryset = DocumentType.objects.all()

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_create, queryset=queryset,
            user=self.request.user
        )

        serializer.validated_data['document_type'] = get_object_or_404(
            queryset=queryset, pk=serializer.validated_data['document_type_id']
        )
        super().perform_create(serializer=serializer)

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APIDocumentChangeTypeView(generics.GenericAPIView):
    """
    post: Change the type of the selected document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_document_properties_edit,),
    }
    queryset = Document.objects.all()
    serializer_class = DocumentChangeTypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_type = DocumentType.objects.get(
            pk=request.data['document_type_id']
        )
        self.get_object().document_type_change(
            document_type=document_type, _user=self.request.user
        )
        return Response(status=status.HTTP_200_OK)


class APIDocumentUploadView(generics.CreateAPIView):
    """
    post: Create a new document and a new document file.
    """
    serializer_class = DocumentUploadSerializer

    def perform_create(self, serializer):
        queryset = DocumentType.objects.all()

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_create, queryset=queryset,
            user=self.request.user
        )

        serializer.validated_data['document_type'] = get_object_or_404(
            queryset=queryset, pk=serializer.validated_data['document_type_id']
        )
        super().perform_create(serializer=serializer)

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }
