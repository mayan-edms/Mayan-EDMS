import logging

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.converter.api_view_mixins import APIImageViewMixin
from mayan.apps.rest_api import generics

from ..models.trashed_document_models import TrashedDocument
from ..permissions import (
    permission_document_version_view, permission_document_view,
    permission_trashed_document_delete, permission_trashed_document_restore
)
from ..serializers.trashed_document_serializers import TrashedDocumentSerializer
from ..tasks import task_trashed_document_delete

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        task_trashed_document_delete.apply_async(
            kwargs={
                'trashed_document_id': instance.pk,
                'user_id': self.request.user.pk
            }
        )

        return Response(status=status.HTTP_202_ACCEPTED)


class APITrashedDocumentListView(generics.ListAPIView):
    """
    get: Returns a list of all the trashed documents.
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


class APITrashedDocumentImageView(
    APIImageViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected trashed document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'GET': (permission_document_version_view,),
    }

    def get_queryset(self):
        return TrashedDocument.objects.all()

    def get_object(self):
        from rest_framework.generics import get_object_or_404

        obj = super().get_object()

        # Return a 404 if the document doesn't have any pages.
        first_page = obj.pages.first()

        if first_page:
            first_page_id = first_page.pk
        else:
            first_page_id = None

        return get_object_or_404(queryset=obj.pages, pk=first_page_id)
