from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers import DocumentSerializer
from mayan.apps.rest_api import generics

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
    queryset = Index.objects.all()
    serializer_class = IndexSerializer


class APIIndexNodeInstanceDocumentListView(generics.ListAPIView):
    """
    Returns a list of all the documents contained by a particular index node
    instance.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        index_node_instance = get_object_or_404(
            klass=IndexInstanceNode, pk=self.kwargs['pk']
        )
        AccessControlList.objects.check_access(
            obj=index_node_instance.index,
            permissions=(permission_document_indexing_view,),
            user=self.request.user
        )

        return index_node_instance.documents.all()


class APIIndexTemplateListView(generics.ListAPIView):
    """
    get: Returns a list of all the template nodes for the selected index.
    """
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    serializer_class = IndexTemplateNodeSerializer


class APIIndexTemplateView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected index template node.
    get: Returns the details of the selected index template node.
    patch: Partially edit an index template node.
    put: Edit an index template node.
    """
    mayan_object_permissions = {
        'GET': (permission_document_indexing_view,),
        'PUT': (permission_document_indexing_edit,),
        'PATCH': (permission_document_indexing_edit,),
        'DELETE': (permission_document_indexing_edit,)
    }
    queryset = IndexTemplateNode.objects.all()
    serializer_class = IndexTemplateNodeSerializer


class APIDocumentIndexListView(generics.ListAPIView):
    """
    Returns a list of all the indexes to which a document belongs.
    """
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    serializer_class = IndexInstanceNodeSerializer

    def get_queryset(self):
        document = get_object_or_404(klass=Document, pk=self.kwargs['pk'])
        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )

        return document.index_instance_nodes.all()
