from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.documents.models import Document, DocumentVersion
from mayan.apps.rest_api import generics

from .models import DocumentPageOCRContent, DocumentTypeSettings
from .permissions import (
    permission_document_type_ocr_setup, permission_ocr_content_view,
    permission_ocr_document,
)
from .serializers import (
    DocumentPageOCRContentSerializer, DocumentTypeOCRSettingsSerializer
)


class APIDocumentTypeOCRSettingsView(generics.RetrieveUpdateAPIView):
    """
    get: Return the document type OCR settings.
    patch: Set the document type OCR settings.
    put: Set the document type OCR settings.
    """
    lookup_field = 'document_type__pk'
    lookup_url_kwarg = 'pk'
    mayan_object_permissions = {
        'GET': (permission_document_type_ocr_setup,),
        'PATCH': (permission_document_type_ocr_setup,),
        'PUT': (permission_document_type_ocr_setup,)
    }
    queryset = DocumentTypeSettings.objects.all()
    serializer_class = DocumentTypeOCRSettingsSerializer


class APIDocumentOCRView(generics.GenericAPIView):
    """
    post: Submit a document for OCR.
    """
    mayan_object_permissions = {
        'POST': (permission_ocr_document,)
    }
    queryset = Document.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr()
        return Response(status=status.HTTP_202_ACCEPTED)


class APIDocumentVersionOCRView(generics.GenericAPIView):
    """
    post: Submit a document version for OCR.
    """
    lookup_url_kwarg = 'version_pk'
    mayan_object_permissions = {
        'POST': (permission_ocr_document,)
    }
    queryset = DocumentVersion.objects.all()

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['document_pk'])

    def get_queryset(self):
        return self.get_document().versions.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        self.get_object().submit_for_ocr()
        return Response(status=status.HTTP_202_ACCEPTED)


class APIDocumentPageOCRContentView(generics.RetrieveAPIView):
    """
    get: Returns the OCR content of the selected document page.
    """
    lookup_url_kwarg = 'page_pk'
    mayan_object_permissions = {
        'GET': (permission_ocr_content_view,),
    }
    serializer_class = DocumentPageOCRContentSerializer

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['document_pk'])

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document().versions.all(),
            pk=self.kwargs['version_pk']
        )

    def get_queryset(self):
        return self.get_document_version().pages.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            ocr_content = instance.ocr_content
        except DocumentPageOCRContent.DoesNotExist:
            ocr_content = DocumentPageOCRContent.objects.none()

        serializer = self.get_serializer(ocr_content)
        return Response(serializer.data)
