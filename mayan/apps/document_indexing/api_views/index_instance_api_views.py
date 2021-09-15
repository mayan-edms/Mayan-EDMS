from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers.document_serializers import DocumentSerializer
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from ..models import IndexInstance
from ..permissions import permission_index_instance_view
from ..serializers import (
    IndexInstanceNodeSerializer, IndexInstanceSerializer
)


class APIDocumentIndexInstanceNodeListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the indexes instance nodes where this
    document is found.
    """
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    mayan_external_object_permissions = {
        'GET': (permission_index_instance_view,)
    }
    mayan_object_permissions = {
        'GET': (permission_index_instance_view,)
    }
    serializer_class = IndexInstanceNodeSerializer

    def get_queryset(self):
        return self.external_object.index_instance_nodes.all()


class APIIndexInstanceDetailView(generics.RetrieveAPIView):
    """
    get: Returns the details of the selected index instance.
    """
    lookup_url_kwarg = 'index_instance_id'
    mayan_object_permissions = {'GET': (permission_index_instance_view,)}
    queryset = IndexInstance.objects.all()
    serializer_class = IndexInstanceSerializer


class APIIndexInstanceListView(generics.ListAPIView):
    """
    get: Returns a list of all the indexes instances.
    """
    mayan_object_permissions = {'GET': (permission_index_instance_view,)}
    queryset = IndexInstance.objects.all()
    serializer_class = IndexInstanceSerializer


class APIIndexInstanceNodeViewMixin:
    serializer_class = IndexInstanceNodeSerializer

    def get_index_instance(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_index_instance_view,
            queryset=IndexInstance.objects.all(), user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['index_instance_id']
        )


class APIIndexInstanceNodeListView(
    APIIndexInstanceNodeViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the nodes for the selected index instance.
    """
    ordering_fields = ('id', 'values')

    def get_queryset(self):
        return self.get_index_instance().get_children()


class APIIndexInstanceNodeDetailView(
    APIIndexInstanceNodeViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns the details of the selected index instance node.
    """
    lookup_url_kwarg = 'index_instance_node_id'

    def get_queryset(self):
        return self.get_index_instance().get_descendants()


class APIIndexInstanceNodeChildrenNodeListView(
    APIIndexInstanceNodeViewMixin, generics.ListAPIView
):
    """
    get: Returns list of all the children nodes for the selected index
    instance node.
    """
    lookup_url_kwarg = 'index_instance_node_id'

    def get_node(self):
        return get_object_or_404(
            klass=self.get_index_instance().get_descendants(),
            pk=self.kwargs['index_instance_node_id']
        )

    def get_queryset(self):
        return self.get_node().get_children()


class APIIndexInstanceNodeDocumentListView(
    APIIndexInstanceNodeViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the documents contained by a particular
    index instance node.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_node(self):
        return get_object_or_404(
            klass=self.get_index_instance().get_descendants(),
            pk=self.kwargs['index_instance_node_id']
        )

    def get_queryset(self):
        return Document.valid.filter(
            pk__in=self.get_node().documents.values('pk')
        )
