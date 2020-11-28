from mayan.apps.rest_api import generics

from ..models.document_models import RecentlyCreatedDocument
from ..permissions import permission_document_view
from ..serializers.document_serializers import DocumentSerializer


class APIRecentlyCreatedDocumentListView(generics.ListAPIView):
    """
    get: Return a list of the recently created documents.
    """
    mayan_object_permissions = {
        'GET': (permission_document_view,)
    }
    queryset = RecentlyCreatedDocument.recently_created.all()
    serializer_class = DocumentSerializer
