import logging

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.converter.api_view_mixins import APIImageViewMixin
from mayan.apps.rest_api import generics
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.views.generics import DownloadViewMixin

from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_edit, permission_document_file_new,
    permission_document_file_view
)
from ..serializers.document_file_serializers import (
    DocumentFileSerializer, DocumentFilePageSerializer
)
from ..tasks import task_document_file_upload

from .mixins import (
    ParentObjectDocumentAPIViewMixin, ParentObjectDocumentFileAPIViewMixin
)

logger = logging.getLogger(name=__name__)


class APIDocumentFileListView(
    ParentObjectDocumentAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Return a list of the selected document's files.
    post: Create a new document file.
    """
    ordering_fields = ('comment', 'encoding', 'id', 'mime_type')
    serializer_class = DocumentFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_202_ACCEPTED)

    def perform_create(self, serializer):
        shared_uploaded_file = SharedUploadedFile.objects.create(
            file=serializer.validated_data['file_new']
        )

        task_document_file_upload.apply_async(
            kwargs={
                'action': serializer.validated_data['action'],
                'comment': serializer.validated_data.get('comment', ''),
                'document_id': self.get_document(
                    permission=permission_document_file_new
                ).pk,
                'filename': serializer.validated_data.get('filename', ''),
                'shared_uploaded_file_id': shared_uploaded_file.pk,
                'user_id': self.request.user.pk
            }
        )

    def get_queryset(self):
        return self.get_document(
            permission=permission_document_file_view
        ).files.all()


class APIDocumentFileDetailView(
    ParentObjectDocumentAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected document file.
    get: Returns the selected document file details.
    """
    lookup_url_kwarg = 'document_file_id'
    mayan_object_permissions = {
        'DELETE': (permission_document_file_delete,),
        'GET': (permission_document_file_view,),
        'PATCH': (permission_document_file_edit,),
        'PUT': (permission_document_file_edit,),
    }
    serializer_class = DocumentFileSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.get_document().files.all()


class APIDocumentFileDownloadView(
    DownloadViewMixin, ParentObjectDocumentAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Download a document file.
    """
    lookup_url_kwarg = 'document_file_id'
    mayan_object_permissions = {
        'GET': (permission_document_file_download,),
    }

    def get_download_file_object(self):
        instance = self.get_object()
        instance._event_actor = self.request.user
        return instance.get_download_file_object()

    def get_download_filename(self):
        return self.get_object().filename

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def get_queryset(self):
        return self.get_document().files.all()

    def retrieve(self, request, *args, **kwargs):
        return self.render_to_response()


# Document file page


class APIDocumentFilePageDetailView(
    ParentObjectDocumentFileAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns the selected document page details.
    """
    lookup_url_kwarg = 'document_file_page_id'
    serializer_class = DocumentFilePageSerializer
    mayan_object_permissions = {
        'GET': (permission_document_file_view,),
    }

    def get_queryset(self):
        return self.get_document_file().pages.all()


class APIDocumentFilePageImageView(
    APIImageViewMixin, ParentObjectDocumentFileAPIViewMixin,
    generics.RetrieveAPIView
):
    """
    get: Returns an image representation of the selected document.
    """
    lookup_url_kwarg = 'document_file_page_id'
    mayan_object_permissions = {
        'GET': (permission_document_file_view,),
    }

    def get_queryset(self):
        return self.get_document_file().pages.all()


class APIDocumentFilePageListView(
    ParentObjectDocumentFileAPIViewMixin, generics.ListAPIView
):
    serializer_class = DocumentFilePageSerializer

    def get_queryset(self):
        return self.get_document_file(
            permission=permission_document_file_view
        ).pages.all()
