import logging

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api import generics

from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..models.misc_models import DeletedDocument, RecentDocument
from ..permissions import (
    permission_document_create, permission_document_properties_edit,
    permission_document_trash, permission_document_view,
    permission_trashed_document_delete, permission_trashed_document_restore
)
from ..serializers.document_serializers import (
    DocumentSerializer, DocumentCreateSerializer,
    DocumentTypeChangeSerializer, DocumentWritableSerializer,
    RecentDocumentSerializer, TrashedDocumentSerializer
)

logger = logging.getLogger(name=__name__)


class APIDocumentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the documents.
    post: Create a new document.
    """
    mayan_object_permissions = {
        'GET': (permission_document_view,),
    }
    queryset = Document.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        elif self.request.method == 'POST':
            return DocumentCreateSerializer

    def perform_create(self, serializer):
        AccessControlList.objects.check_access(
            obj=serializer.validated_data['document_type'],
            permissions=(permission_document_create,), user=self.request.user
        )
        super().perform_create(serializer=serializer)

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentSerializer
        else:
            return DocumentWritableSerializer


class APIDocumentTypeChangeView(generics.GenericAPIView):
    """
    post: Change the type of the selected document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_document_properties_edit,),
    }
    queryset = Document.objects.all()
    serializer_class = DocumentTypeChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document_type = DocumentType.objects.get(pk=request.data['new_document_type'])
        self.get_object().document_type_change(
            document_type=document_type, _user=self.request.user
        )
        return Response(status=status.HTTP_200_OK)


class APIRecentDocumentListView(generics.ListAPIView):
    """
    get: Return a list of the recent documents for the current user.
    """
    serializer_class = RecentDocumentSerializer

    def get_queryset(self):
        return RecentDocument.objects.filter(user=self.request.user)


class APITrashedDocumentDetailView(generics.RetrieveDestroyAPIView):
    """
    Returns the selected trashed document details.
    delete: Delete the trashed document.
    get: Retreive the details of the trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'DELETE': (permission_trashed_document_delete,),
        'GET': (permission_document_view,)
    }
    queryset = DeletedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the trashed documents.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    queryset = DeletedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentRestoreView(generics.GenericAPIView):
    """
    post: Restore a trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_trashed_document_restore,)
    }
    queryset = DeletedDocument.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, *args, **kwargs):
        self.get_object().restore()
        return Response(status=status.HTTP_200_OK)
