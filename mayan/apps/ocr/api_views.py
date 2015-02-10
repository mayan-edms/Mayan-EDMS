from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from acls.models import AccessEntry
from documents.models import DocumentVersion
from permissions.models import Permission
from rest_api.permissions import MayanPermission

from .permissions import PERMISSION_OCR_DOCUMENT
from .serializers import DocumentVersionOCRSerializer


class DocumentVersionOCRView(generics.GenericAPIView):
    serializer_class = DocumentVersionOCRSerializer

    permission_classes = (MayanPermission,)

    def post(self, request, *args, **kwargs):
        """Submit document version for OCR."""

        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            document_version = get_object_or_404(DocumentVersion, pk=serializer.data['document_version_id'])

            try:
                Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])
            except PermissionDenied:
                AccessEntry.objects.check_access(PERMISSION_OCR_DOCUMENT, request.user, document_version.document)

            document_version.submit_for_ocr()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
