from mayan.apps.documents.api_views.mixins import ParentObjectDocumentFilePageAPIViewMixin
from mayan.apps.rest_api import generics

from .models import DocumentFilePageContent, DocumentTypeSettings
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup
)
from .serializers import (
    DocumentFilePageContentSerializer, DocumentTypeParsingSettingsSerializer
)


class APIDocumentFilePageContentView(
    ParentObjectDocumentFilePageAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns the content of the selected document page.
    """
    mayan_object_permissions = {
        'GET': (permission_document_file_content_view,),
    }
    serializer_class = DocumentFilePageContentSerializer

    def get_object(self):
        document_file_page = self.get_document_file_page(
            permission=self.mayan_object_permissions[self.request.method][0]
        )

        try:
            return DocumentFilePageContent.objects.get(
                document_file_page=document_file_page
            )
        except DocumentFilePageContent.DoesNotExist:
            return DocumentFilePageContent(
                document_file_page=document_file_page
            )


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
