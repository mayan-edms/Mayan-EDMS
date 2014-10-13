from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessEntry
from documents.models import Document
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from permissions.models import Permission
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Index, IndexInstanceNode
from .permissions import (PERMISSION_DOCUMENT_INDEXING_CREATE,
                          PERMISSION_DOCUMENT_INDEXING_VIEW)
from .serializers import IndexSerializer


class APIIndexView(generics.RetrieveAPIView):
    """
    Details of the selected index.
    """
    serializer_class = IndexSerializer
    queryset = Index.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW]}


class APIIndexListView(generics.ListCreateAPIView):
    """
    Returns a list of all the defined indexes.
    """

    serializer_class = IndexSerializer
    queryset = Index.objects.all()

    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': [PERMISSION_DOCUMENT_INDEXING_VIEW]}
    mayan_view_permissions = {'POST': [PERMISSION_DOCUMENT_INDEXING_CREATE]}


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
