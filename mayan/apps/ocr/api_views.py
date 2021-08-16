from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_version_models import DocumentVersion
from mayan.apps.rest_api import generics

from .models import DocumentVersionPageOCRContent, DocumentTypeOCRSettings
from .permissions import (
    permission_document_type_ocr_setup, permission_document_version_ocr_content_view,
    permission_document_version_ocr,
)
from .serializers import (
    DocumentVersionPageOCRContentSerializer, DocumentTypeOCRSettingsSerializer
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
    queryset = Document.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr(_user=self.request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class APIDocumentVersionPageOCRContentView(generics.RetrieveAPIView):
    """
    get: Returns the OCR content of the selected document page.
    """
    lookup_url_kwarg = 'document_version_page_id'
    mayan_object_permissions = {
        'GET': (permission_document_version_ocr_content_view,),
    }
    serializer_class = DocumentVersionPageOCRContentSerializer

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['document_id'])

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document().versions.all(),
            pk=self.kwargs['document_version_id']
        )

    def get_queryset(self):
        return self.get_document_version().pages.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            ocr_content = instance.ocr_content
        except DocumentVersionPageOCRContent.DoesNotExist:
            ocr_content = DocumentVersionPageOCRContent.objects.none()

        serializer = self.get_serializer(ocr_content)
        return Response(serializer.data)


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
        return get_object_or_404(klass=Document, pk=self.kwargs['document_id'])

    def get_queryset(self):
        return self.get_document().versions.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr(_user=self.request.user)
        return Response(status=status.HTTP_202_ACCEPTED)
