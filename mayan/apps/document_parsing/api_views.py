from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from mayan.apps.documents.models import Document
from mayan.apps.rest_api import generics

from .models import DocumentFilePageContent, DocumentTypeSettings
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup
)
from .serializers import (
    DocumentFilePageContentSerializer, DocumentTypeParsingSettingsSerializer
)


class APIDocumentFilePageContentView(generics.RetrieveAPIView):
    """
    Returns the content of the selected document page.
    """
    lookup_url_kwarg = 'document_file_page_id'
    mayan_object_permissions = {
        'GET': (permission_document_file_content_view,),
    }
    serializer_class = DocumentFilePageContentSerializer

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['document_id'])

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document().files.all(),
            pk=self.kwargs['document_file_id']
        )

    def get_queryset(self):
        return self.get_document_file().pages.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            content = instance.content
        except DocumentFilePageContent.DoesNotExist:
            content = DocumentFilePageContent.objects.none()

        serializer = self.get_serializer(content)
        return Response(serializer.data)


class APIDocumentTypeParsingSettingsView(generics.RetrieveUpdateAPIView):
    """
    get: Return the document type parsing settings.
    patch: Set the document type parsing settings.
    put: Set the document type parsing settings.
    """
    lookup_field = 'document_type__pk'
    lookup_url_kwarg = 'document_type_id'
    mayan_object_permissions = {
        'GET': (permission_document_type_parsing_setup,),
        'PATCH': (permission_document_type_parsing_setup,),
        'PUT': (permission_document_type_parsing_setup,)
    }
    queryset = DocumentTypeSettings.objects.all()
    serializer_class = DocumentTypeParsingSettingsSerializer
