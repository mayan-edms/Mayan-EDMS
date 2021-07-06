from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers.document_serializers import DocumentSerializer
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import Cabinet
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_remove_document, permission_cabinet_view
)
from .serializers import (
    CabinetDocumentAddSerializer, CabinetDocumentRemoveSerializer,
    CabinetSerializer
)


class APIDocumentCabinetListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    Returns a list of all the cabinets to which a document belongs.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permissions = {'GET': (permission_cabinet_view,)}
    mayan_object_permissions = {'GET': (permission_cabinet_view,)}
    serializer_class = CabinetSerializer

    def get_queryset(self):
        return self.external_object.cabinets.all()


class APICabinetListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the cabinets.
    post: Create a new cabinet.
    """
    mayan_object_permissions = {'GET': (permission_cabinet_view,)}
    mayan_view_permissions = {'POST': (permission_cabinet_create,)}
    ordering_fields = ('id', 'label')
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APICabinetView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected cabinet.
    get: Returns the details of the selected cabinet.
    patch: Edit the selected cabinet.
    put: Edit the selected cabinet.
    """
    lookup_url_kwarg = 'cabinet_id'
    mayan_object_permissions = {
        'GET': (permission_cabinet_view,),
        'PUT': (permission_cabinet_edit,),
        'PATCH': (permission_cabinet_edit,),
        'DELETE': (permission_cabinet_delete,)
    }
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APICabinetDocumentAddView(generics.ObjectActionAPIView):
    """
    post: Add a document to a cabinet.
    """
    lookup_url_kwarg = 'cabinet_id'
    mayan_object_permissions = {
        'POST': (permission_cabinet_add_document,)
    }
    serializer_class = CabinetDocumentAddSerializer
    queryset = Cabinet.objects.all()

    def object_action(self, request, serializer):
        document = serializer.validated_data['document']
        self.object._event_actor = self.request.user
        self.object.document_add(document=document)


class APICabinetDocumentRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a document from a cabinet.
    """
    lookup_url_kwarg = 'cabinet_id'
    mayan_object_permissions = {
        'POST': (permission_cabinet_remove_document,)
    }
    serializer_class = CabinetDocumentRemoveSerializer
    queryset = Cabinet.objects.all()

    def object_action(self, request, serializer):
        document = serializer.validated_data['document']
        self.object._event_actor = self.request.user
        self.object.document_remove(document=document)


class APICabinetDocumentListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the documents contained in a particular cabinet.
    """
    external_object_class = Cabinet
    external_object_pk_url_kwarg = 'cabinet_id'
    mayan_external_object_permissions = {'GET': (permission_cabinet_view,)}
    mayan_object_permissions = {
        'GET': (permission_document_view,),
    }
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.valid.filter(
            pk__in=self.external_object.documents.only('pk')
        )
