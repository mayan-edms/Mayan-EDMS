from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from mayan.apps.documents.models import Document, DocumentVersion
from mayan.apps.rest_api.permissions import MayanPermission

from .models import DocumentVersionPageOCRContent
from .permissions import permission_ocr_content_view, permission_ocr_document
from .serializers import DocumentPageOCRContentSerializer


class APIDocumentOCRView(generics.GenericAPIView):
    """
    post: Submit a document for OCR.
    """
    mayan_object_permissions = {
        'POST': (permission_ocr_document,)
    }
    permission_classes = (MayanPermission,)
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
    permission_classes = (MayanPermission,)
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
    permission_classes = (MayanPermission,)
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
        except DocumentVersionPageOCRContent.DoesNotExist:
            ocr_content = DocumentVersionPageOCRContent.objects.none()

        serializer = self.get_serializer(ocr_content)
        return Response(serializer.data)
