from mayan.apps.rest_api import generics

from ..models.recently_accessed_document_models import RecentlyAccessedDocument
from ..serializers.recently_accessed_document_serializers import (
    RecentlyAccessedDocumentSerializer
)
from ..permissions import permission_document_view


class APIRecentlyAccessedDocumentListView(generics.ListAPIView):
    """
    get: Return a list of the recently accessed documents for the current user.
    """
    mayan_object_permissions = {
        'GET': (permission_document_view,)
    }
    serializer_class = RecentlyAccessedDocumentSerializer

    def get_queryset(self):
        return RecentlyAccessedDocument.objects.filter(user=self.request.user)
