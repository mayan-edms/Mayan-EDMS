from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from mayan.apps.documents.models import Document
from mayan.apps.rest_api import generics

from .models import DocumentPageContent
from .permissions import permission_content_view
from .serializers import DocumentPageContentSerializer


class APIDocumentPageContentView(generics.RetrieveAPIView):
    """
    Returns the content of the selected document page.
    """
    lookup_url_kwarg = 'page_pk'
    mayan_object_permissions = {
        'GET': (permission_content_view,),
    }
    serializer_class = DocumentPageContentSerializer

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
            content = instance.content
        except DocumentPageContent.DoesNotExist:
            content = DocumentPageContent.objects.none()

        serializer = self.get_serializer(content)
        return Response(serializer.data)
