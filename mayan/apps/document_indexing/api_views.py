from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessEntry
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Index, IndexInstanceNode, IndexTemplateNode
from .permissions import (PERMISSION_DOCUMENT_INDEXING_CREATE,
                          PERMISSION_DOCUMENT_INDEXING_DELETE,
                          PERMISSION_DOCUMENT_INDEXING_EDIT,
                          PERMISSION_DOCUMENT_INDEXING_VIEW)
from .serializers import (IndexInstanceNodeSerializer, IndexSerializer,
                          IndexTemplateNodeSerializer)


class APIIndexListView(generics.ListCreateAPIView):
    serializer_class = IndexSerializer
    queryset = Index.objects.all()

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_INDEXING_CREATE]}

    def get(self, *args, **kwargs):
        """Returns a list of all the defined indexes."""
        return super(APIIndexListView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Create a new index."""
        return super(APIIndexListView, self).post(*args, **kwargs)


class APIIndexView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IndexSerializer
    queryset = Index.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW],
        'PUT': [PERMISSION_DOCUMENT_INDEXING_EDIT],
        'PATCH': [PERMISSION_DOCUMENT_INDEXING_EDIT],
        'DELETE': [PERMISSION_DOCUMENT_INDEXING_DELETE]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected index."""
        return super(APIIndexView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Returns the details of the selected index."""
        return super(APIIndexView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Partially edit an index."""
        return super(APIIndexView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit an index."""
        return super(APIIndexView, self).put(*args, **kwargs)


class APIIndexNodeInstanceDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents contained by a particular index node instance.
    """

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_VIEW]}

    def get_serializer_class(self):
        from documents.serializers import DocumentSerializer
        return DocumentSerializer

    def get_queryset(self):
        index_node_instance = get_object_or_404(IndexInstanceNode, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_INDEXING_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_INDEXING_VIEW, self.request.user, index_node_instance.index)

        return index_node_instance.documents.all()


class APIIndexTemplateListView(generics.ListAPIView):
    serializer_class = IndexTemplateNodeSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW]}

    def get(self, *args, **kwargs):
        """Returns a list of all the template nodes for the selected index."""
        return super(APIIndexTemplateListView, self).get(*args, **kwargs)


class APIIndexTemplateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IndexTemplateNodeSerializer
    queryset = IndexTemplateNode.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW],
        'PUT': [PERMISSION_DOCUMENT_INDEXING_EDIT],
        'PATCH': [PERMISSION_DOCUMENT_INDEXING_EDIT],
        'DELETE': [PERMISSION_DOCUMENT_INDEXING_EDIT]
    }

    def delete(self, *args, **kwargs):
        """Delete the selected index template node."""
        return super(APIIndexTemplateView, self).delete(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Returns the details of the selected index template node."""
        return super(APIIndexTemplateView, self).get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Partially edit an index template node."""
        return super(APIIndexTemplateView, self).patch(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Edit an index template node."""
        return super(APIIndexTemplateView, self).put(*args, **kwargs)


class APIDocumentIndexListView(generics.ListAPIView):
    """
    Returns a list of all the indexes to which a document belongs.
    """

    serializer_class = IndexInstanceNodeSerializer

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW]}

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_DOCUMENT_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, self.request.user, document)

        return document.node_instances.all()
