from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from acls.models import AccessControlList
from documents.models import Document, DocumentPage, DocumentVersion
from permissions import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import DocumentPageContent
from .permissions import permission_ocr_content_view, permission_ocr_document
from .serializers import DocumentPageContentSerializer


class DocumentOCRAPIView(APIView):
    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """
        Submit a document for OCR.
        ---
        omit_serializer: true
        parameters:
            - name: pk
              paramType: path
              type: number
        responseMessages:
            - code: 202
              message: Accepted
        """

        document = self.get_object()
        try:
            Permission.check_permissions(
                self.request.user, (permission_ocr_document,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_ocr_document, self.request.user, document
            )

        document.submit_for_ocr()
        return Response(status=status.HTTP_202_ACCEPTED)


class DocumentVersionOCRAPIView(APIView):
    def get_object(self):
        return get_object_or_404(DocumentVersion, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """
        Submit a document version for OCR.
        ---
        omit_serializer: true
        parameters:
            - name: pk
              paramType: path
              type: number
        responseMessages:
            - code: 202
              message: Accepted
        """

        document_version = self.get_object()
        try:
            Permission.check_permissions(
                self.request.user, (permission_ocr_document,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_ocr_document, self.request.user, document_version
            )

        document_version.submit_for_ocr()
        return Response(status=status.HTTP_202_ACCEPTED)


class DocumentPageContentAPIView(generics.RetrieveAPIView):
    """
    Returns the OCR content of the selected document page.
    ---
    GET:
        parameters:
            - name: pk
              paramType: path
              type: number
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {
        'GET': (permission_ocr_content_view,),
    }
    permission_classes = (MayanPermission,)
    serializer_class = DocumentPageContentSerializer

    def get_object(self):
        document_page = get_object_or_404(DocumentPage, pk=self.kwargs['pk'])
        try:
            return document_page.ocr_content
        except DocumentPageContent.DoesNotExist:
            return DocumentPageContent.objects.none()
