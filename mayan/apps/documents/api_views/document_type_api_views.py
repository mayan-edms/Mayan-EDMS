import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, patch_cache_control

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api import generics
from mayan.apps.views.generics import DownloadMixin

from ..literals import DOCUMENT_IMAGE_TASK_TIMEOUT
from ..models.document_file_models import DocumentFile
from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..models.misc_models import DeletedDocument, RecentDocument
from ..permissions import (
    permission_document_create, permission_document_edit,
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_new,  permission_document_file_view,
    permission_document_properties_edit, permission_document_trash,
    permission_document_type_create, permission_document_type_delete,
    permission_document_type_edit, permission_document_type_view,
    permission_document_view, permission_trashed_document_delete,
    permission_trashed_document_restore
)
from ..serializers.document_serializers import DocumentSerializer
from ..serializers.document_type_serializers import (
    DocumentTypeSerializer, DocumentTypeWritableSerializer
)
from ..settings import (
    setting_document_file_page_image_cache_time,
    setting_document_version_page_image_cache_time
)
from ..tasks import (
    task_document_file_page_image_generate,
    task_document_version_page_image_generate
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
