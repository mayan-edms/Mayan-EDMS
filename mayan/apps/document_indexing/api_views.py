from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view
from documents.serializers import DocumentSerializer
from rest_api.filters import MayanObjectPermissionsFilter
from rest_api.permissions import MayanPermission

from .models import Index, IndexInstanceNode, IndexTemplateNode
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit, permission_document_indexing_view
)
from .serializers import (
    IndexInstanceNodeSerializer, IndexSerializer, IndexTemplateNodeSerializer
)


class APIIndexListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the defined indexes.
    post: Create a new index.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    mayan_view_permissions = {'POST': (permission_document_indexing_create,)}
    queryset = Index.objects.all()
    serializer_class = IndexSerializer


class APIIndexView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected index.
    get: Returns the details of the selected index.
    patch: Partially edit an index.
    put: Edit an index.
    """
    mayan_object_permissions = {
        'GET': (permission_document_indexing_view,),
        'PUT': (permission_document_indexing_edit,),
        'PATCH': (permission_document_indexing_edit,),
        'DELETE': (permission_document_indexing_delete,)
    }
    permission_classes = (MayanPermission,)
    queryset = Index.objects.all()
    serializer_class = IndexSerializer


class APIIndexNodeInstanceDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents contained by a particular index node
    instance.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        index_node_instance = get_object_or_404(
            IndexInstanceNode, pk=self.kwargs['pk']
        )
        AccessControlList.objects.check_access(
            permissions=permission_document_indexing_view,
            user=self.request.user, obj=index_node_instance.index
        )

        return index_node_instance.documents.all()


class APIIndexTemplateListView(generics.ListAPIView):
    """
    get: Returns a list of all the template nodes for the selected index.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    serializer_class = IndexTemplateNodeSerializer


class APIIndexTemplateView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected index template node.
    get: Returns the details of the selected index template node.
    patch: Partially edit an index template node.
    put: Edit an index template node.
    """
    serializer_class = IndexTemplateNodeSerializer
    queryset = IndexTemplateNode.objects.all()

    permission_classes = (MayanPermission,)
    mayan_object_permissions = {
        'GET': (permission_document_indexing_view,),
        'PUT': (permission_document_indexing_edit,),
        'PATCH': (permission_document_indexing_edit,),
        'DELETE': (permission_document_indexing_edit,)
    }


class APIDocumentIndexListView(generics.ListAPIView):
    """
    Returns a list of all the indexes to which a document belongs.
    """
    filter_backends = (MayanObjectPermissionsFilter,)
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    serializer_class = IndexInstanceNodeSerializer

    def get_queryset(self):
        document = get_object_or_404(Document, pk=self.kwargs['pk'])
        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=self.request.user,
            obj=document
        )

        return document.index_instance_nodes.all()
