import logging

from mayan.apps.rest_api import generics

from ..models.trashed_document_models import TrashedDocument
from ..permissions import (
    permission_document_view, permission_trashed_document_delete,
    permission_trashed_document_restore
)
from ..serializers.trashed_document_serializers import TrashedDocumentSerializer

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

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APITrashedDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the trashed documents.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    ordering_fields = ('id', 'label')
    queryset = TrashedDocument.objects.all()
    serializer_class = TrashedDocumentSerializer


class APITrashedDocumentRestoreView(generics.ObjectActionAPIView):
    """
    post: Restore a trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_trashed_document_restore,)
    }
    queryset = TrashedDocument.objects.all()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def object_action(self, request, serializer):
        self.object.restore()
