from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers.document_serializers import (
    DocumentSerializer
)
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)
from .serializers import (
    DocumentTagAttachSerializer, DocumentTagRemoveSerializer,
    TagSerializer
)


class APITagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected tag.
    get: Return the details of the selected tag.
    patch: Edit the selected tag.
    put: Edit the selected tag.
    """
    lookup_url_kwarg = 'tag_id'
    mayan_object_permissions = {
        'DELETE': (permission_tag_delete,),
        'GET': (permission_tag_view,),
        'PATCH': (permission_tag_edit,),
        'PUT': (permission_tag_edit,)
    }
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APITagListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the tags.
    post: Create a new tag.
    """
    mayan_object_permissions = {'GET': (permission_tag_view,)}
    mayan_view_permissions = {'POST': (permission_tag_create,)}
    ordering_fields = ('id', 'label')
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APITagDocumentListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the documents tagged by a particular tag.
    """
    external_object_class = Tag
    external_object_pk_url_kwarg = 'tag_id'
    mayan_external_object_permissions = {'GET': (permission_tag_view,)}
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.valid.filter(
            pk__in=self.external_object.documents.only('pk')
        )


class APIDocumentTagAttachView(generics.ObjectActionAPIView):
    """
    post: Attach a tag to a document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_tag_attach,)
    }
    serializer_class = DocumentTagAttachSerializer
    queryset = Document.valid

    def object_action(self, request, serializer):
        tag = serializer.validated_data['tag']
        tag._event_actor = self.request.user
        tag.attach_to(document=self.object)


class APIDocumentTagRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a tag from a document.
    """
    lookup_url_kwarg = 'document_id'
    mayan_object_permissions = {
        'POST': (permission_tag_remove,)
    }
    serializer_class = DocumentTagRemoveSerializer
    queryset = Document.valid

    def object_action(self, request, serializer):
        tag = serializer.validated_data['tag']
        tag._event_actor = self.request.user
        tag.remove_from(document=self.object)


class APIDocumentTagListView(ExternalObjectAPIViewMixin, generics.ListAPIView):
    """
    get: Returns a list of all the tags attached to a document.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permissions = {
        'GET': (permission_tag_view,)
    }
    mayan_object_permissions = {
        'GET': (permission_tag_view,),
    }
    serializer_class = TagSerializer

    def get_queryset(self):
        return self.external_object.tags.all()
