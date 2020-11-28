import logging

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.rest_api import generics

from ..models.document_models import TrashedDocument
from ..permissions import (
    permission_document_view, permission_trashed_document_delete,
    permission_trashed_document_restore
)
from ..serializers.document_serializers import TrashedDocumentSerializer

logger = logging.getLogger(name=__name__)


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
    queryset = TrashedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the trashed documents.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    queryset = TrashedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentRestoreView(generics.GenericAPIView):
    """
    post: Restore a trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_trashed_document_restore,)
    }
    queryset = TrashedDocument.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, *args, **kwargs):
        self.get_object().restore()
        return Response(status=status.HTTP_200_OK)
