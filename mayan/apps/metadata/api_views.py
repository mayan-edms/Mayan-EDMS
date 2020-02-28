from __future__ import absolute_import, unicode_literals

from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_view, permission_document_type_edit
)
from mayan.apps.rest_api.mixins import ExternalObjectAPIViewSetMixin
from mayan.apps.rest_api.viewsets import MayanModelAPIViewSet

from .models import MetadataType
from .permissions import (
    permission_metadata_add, permission_metadata_remove,
    permission_metadata_edit, permission_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .serializers import (
    DocumentMetadataSerializer, DocumentTypeMetadataTypeRelationSerializer,
    MetadataTypeSerializer, MetadataTypeDocumentTypeRelationSerializer
)


class DocumentMetadataAPIViewSet(
    ExternalObjectAPIViewSetMixin, MayanModelAPIViewSet
):
    external_object_class = Document
    external_object_pk_url_kwarg = 'document_id'
    lookup_url_kwarg = 'document_metadata_id'
    object_permission_map = {
        'list': permission_metadata_view,
        'partial_update': permission_metadata_edit,
        'destroy': permission_metadata_remove,
        'retrieve': permission_metadata_view,
        'update': permission_metadata_edit,
    }
    serializer_class = DocumentMetadataSerializer

    def get_external_object_permission(self):
        # Custom permission map for the Document instance
        action = getattr(self, 'action', None)
        if action is None:
            return None
        elif action == 'create':
            return permission_metadata_add
        elif action == 'destroy':
            return permission_metadata_remove
        elif action in ['partial_update', 'update']:
            return permission_metadata_edit
        else:
            return permission_metadata_view

    def get_queryset(self):
        return self.get_external_object().metadata.all()


class DocumentTypeMetadataTypeRelationAPIViewSet(
    ExternalObjectAPIViewSetMixin, MayanModelAPIViewSet
):
    external_object_class = DocumentType
    external_object_pk_url_kwarg = 'document_type_id'
    lookup_url_kwarg = 'document_type_metadata_type_relation_id'
    object_permission_map = {
        'destroy': permission_metadata_type_edit,
        'list': permission_metadata_type_view,
        'partial_update': permission_metadata_type_edit,
        'retrieve': permission_metadata_type_view,
        'update': permission_metadata_type_edit,
    }
    serializer_class = DocumentTypeMetadataTypeRelationSerializer

    def get_external_object_permission(self):
        # Extenal object permissions: Document type
        action = getattr(self, 'action', None)
        if action is None:
            return None
        elif action in ['list', 'retrieve']:
            return permission_document_type_view
        else:
            return permission_document_type_edit

    def get_queryset(self):
        return self.get_external_object().metadata_type_relations.all()


class MetadataTypeAPIViewSet(MayanModelAPIViewSet):
    lookup_url_kwarg = 'metadata_type_id'
    object_permission_map = {
        'destroy': permission_metadata_type_delete,
        'list': permission_metadata_type_view,
        'partial_update': permission_metadata_type_edit,
        'retrieve': permission_metadata_type_view,
        'update': permission_metadata_type_edit,
    }
    queryset = MetadataType.objects.all()
    serializer_class = MetadataTypeSerializer
    view_permission_map = {
        'create': permission_metadata_type_create
    }


class MetadataTypeDocumentTypeRelationAPIViewSet(
    ExternalObjectAPIViewSetMixin, MayanModelAPIViewSet
):
    external_object_class = MetadataType
    external_object_pk_url_kwarg = 'metadata_type_id'
    lookup_url_kwarg = 'metadata_type_document_type_relation_id'
    object_permission_map = {
        'destroy': permission_document_type_edit,
        'list': permission_document_type_view,
        'partial_update': permission_document_type_edit,
        'retrieve': permission_document_type_view,
        'update': permission_document_type_edit,
    }
    serializer_class = MetadataTypeDocumentTypeRelationSerializer

    def get_external_object_permission(self):
        # Extenal object permissions: Metadata type
        action = getattr(self, 'action', None)
        if action is None:
            return None
        elif action in ['list', 'retrieve']:
            return permission_metadata_type_view
        else:
            return permission_metadata_type_edit

    def get_queryset(self):
        return self.get_external_object().document_type_relations.all()
