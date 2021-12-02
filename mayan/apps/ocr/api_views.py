from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from mayan.apps.documents.api_views.mixins import ParentObjectDocumentVersionPageAPIViewMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_version_models import DocumentVersion
from mayan.apps.rest_api import generics

from .models import DocumentVersionPageOCRContent, DocumentTypeOCRSettings
from .permissions import (
    permission_document_type_ocr_setup,
    permission_document_version_ocr_content_edit,
    permission_document_version_ocr_content_view,
    permission_document_version_ocr
)
from .serializers import (
    DocumentVersionPageOCRContentSerializer,
    DocumentTypeOCRSettingsSerializer
)


class APIDocumentTypeOCRSettingsView(generics.RetrieveUpdateAPIView):
    """
    get: Return the document type OCR settings.
    patch: Set the document type OCR settings.
    put: Set the document type OCR settings.
    """
    lookup_field = 'document_type__pk'
    lookup_url_kwarg = 'document_type_id'
    mayan_object_permissions = {
        'GET': (permission_document_type_ocr_setup,),
        'PATCH': (permission_document_type_ocr_setup,),
        'PUT': (permission_document_type_ocr_setup,)
    }
    queryset = DocumentTypeOCRSettings.objects.all()
    serializer_class = DocumentTypeOCRSettingsSerializer


class APIDocumentOCRSubmitView(generics.GenericAPIView):
    """
    post: Submit a document for OCR.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_document_version_ocr,)
    }
    queryset = Document.valid.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr(_user=self.request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class APIDocumentVersionPageOCRContentDetailView(
    ParentObjectDocumentVersionPageAPIViewMixin,
    generics.RetrieveUpdateAPIView
):
    """
    get: Returns the OCR content of the selected document page.
    patch: Edit the OCR content of the selected document page.
    put: Edit the OCR content of the selected document page.
    """
    mayan_object_permissions = {
        'GET': (permission_document_version_ocr_content_view,),
        'PATCH': (permission_document_version_ocr_content_edit,),
        'PUT': (permission_document_version_ocr_content_edit,)
    }
    serializer_class = DocumentVersionPageOCRContentSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_object(self):
        document_version_page = self.get_document_version_page(
            permission=self.mayan_object_permissions.get(
                self.request.method, (None,)
            )[0]
        )

        try:
            return document_version_page.ocr_content
        except DocumentVersionPageOCRContent.DoesNotExist:
            return DocumentVersionPageOCRContent(
                document_version_page=document_version_page
            )


class APIDocumentVersionOCRSubmitView(generics.GenericAPIView):
    """
    post: Submit a document version for OCR.
    """
    lookup_url_kwarg = 'document_version_id'
    mayan_object_permissions = {
        'POST': (permission_document_version_ocr,)
    }
    queryset = DocumentVersion.objects.all()

    def get_document(self):
        return get_object_or_404(
            queryset=Document.valid.all(), pk=self.kwargs['document_id']
        )

    def get_queryset(self):
        return self.get_document().versions.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr(_user=self.request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
