from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers import DocumentSerializer
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.mixins import AsymmetricSerializerViewMixin

from .models import Index, IndexInstance
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_view
)
from .serializers import (
    IndexInstanceNodeSerializer, IndexInstanceSerializer,
    IndexTemplateSerializer, IndexTemplateNodeSerializer,
    IndexTemplateNodeWriteSerializer, IndexTemplateWriteSerializer
)


class APIDocumentIndexInstanceNodeListView(generics.ListAPIView):
    """
    Returns a list of all the indexes instance nodes where this document is found.
    """
    mayan_object_permissions = {'GET': (permission_document_indexing_instance_view,)}
    serializer_class = IndexInstanceNodeSerializer

    def get_document(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view,
            queryset=Document.objects.all(), user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['document_id']
        )

    def get_queryset(self):
        return self.get_document().index_instance_nodes.all()


class APIIndexInstanceDetailView(generics.RetrieveAPIView):
    """
    get: Returns the details of the selected index instance.
    """
    lookup_url_kwarg = 'index_instance_id'
    mayan_object_permissions = {'GET': (permission_document_indexing_instance_view,)}
    queryset = IndexInstance.objects.all()
    serializer_class = IndexInstanceSerializer


class APIIndexInstanceListView(generics.ListAPIView):
    """
    get: Returns a list of all the indexes instances.
    """
    mayan_object_permissions = {'GET': (permission_document_indexing_instance_view,)}
    queryset = IndexInstance.objects.all()
    serializer_class = IndexInstanceSerializer


class APIIndexInstanceNodeViewMixin:
    serializer_class = IndexInstanceNodeSerializer

    def get_index_instance(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_indexing_instance_view,
            queryset=IndexInstance.objects.all(), user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['index_instance_id']
        )


class APIIndexInstanceNodeListView(
    APIIndexInstanceNodeViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the template nodes for the selected index.
    post: Create a new index template node.
    """
    def get_queryset(self):
        return self.get_index_instance().get_children()


class APIIndexInstanceNodeDetailView(
    APIIndexInstanceNodeViewMixin, generics.RetrieveAPIView
):
    """
    delete: Delete the selected index template node.
    get: Returns the details of the selected index template node.
    patch: Partially edit an index template node.
    put: Edit an index template node.
    """
    lookup_url_kwarg = 'index_instance_node_id'

    def get_queryset(self):
        return self.get_index_instance().get_nodes()


class APIIndexInstanceNodeDocumentListView(
    APIIndexInstanceNodeViewMixin, generics.ListAPIView
):
    """
    Returns a list of all the documents contained by a particular index node
    instance.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_node(self):
        return get_object_or_404(
            klass=self.get_index_instance().get_nodes(),
            pk=self.kwargs['index_instance_node_id']
        )

    def get_queryset(self):
        return self.get_node().documents.all()


class APIIndexTemplateViewMixin(AsymmetricSerializerViewMixin):
    queryset = Index.objects.all()
    read_serializer_class = IndexTemplateSerializer
    write_serializer_class = IndexTemplateWriteSerializer


class APIIndexTemplateListView(
    APIIndexTemplateViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the defined indexes template.
    post: Create a new index template.
    """
    mayan_object_permissions = {'GET': (permission_document_indexing_view,)}
    mayan_view_permissions = {'POST': (permission_document_indexing_create,)}
    queryset = Index.objects.all()


class APIIndexTemplateDetailView(
    APIIndexTemplateViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected index template.
    get: Returns the details of the selected index template.
    patch: Partially edit an index template.
    put: Edit an index template.
    """
    lookup_url_kwarg = 'index_template_id'
    mayan_object_permissions = {
        'GET': (permission_document_indexing_view,),
        'PUT': (permission_document_indexing_edit,),
        'PATCH': (permission_document_indexing_edit,),
        'DELETE': (permission_document_indexing_delete,)
    }
    queryset = Index.objects.all()


class APIIndexTemplateNodeViewMixin(AsymmetricSerializerViewMixin):
    object_permissions = {
        'GET': permission_document_indexing_view,
        'PATCH': permission_document_indexing_edit,
        'PUT': permission_document_indexing_edit,
        'POST': permission_document_indexing_edit,
        'DELETE': permission_document_indexing_edit
    }
    read_serializer_class = IndexTemplateNodeSerializer
    write_serializer_class = IndexTemplateNodeWriteSerializer

    def get_index_template(self):
        permission = self.object_permissions[self.request.method]

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Index.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['index_template_id']
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['index_template'] = self.get_index_template()
        return context


class APIIndexTemplateNodeListView(
    APIIndexTemplateNodeViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the template nodes for the selected index.
    post: Create a new index template node.
    """
    def get_queryset(self):
        return self.get_index_template().template_root.get_children()


class APIIndexTemplateNodeDetailView(
    APIIndexTemplateNodeViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected index template node.
    get: Returns the details of the selected index template node.
    patch: Partially edit an index template node.
    put: Edit an index template node.
    """
    lookup_url_kwarg = 'index_template_node_id'

    def get_queryset(self):
        return self.get_index_template().node_templates.all()
