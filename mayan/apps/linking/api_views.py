from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_view, permission_document_view
)
from mayan.apps.documents.serializers.document_type_serializers import DocumentTypeSerializer
from mayan.apps.rest_api import generics
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin

from .models import SmartLink
from .permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)
from .serializers import (
    ResolvedSmartLinkDocumentSerializer, ResolvedSmartLinkSerializer,
    SmartLinkConditionSerializer, SmartLinkDocumentTypeAddSerializer,
    SmartLinkDocumentTypeRemoveSerializer, SmartLinkSerializer
)


class APIResolvedSmartLinkDocumentListView(generics.ListAPIView):
    """
    get: Returns a list of the smart link documents that apply to the document.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = ResolvedSmartLinkDocumentSerializer

    def get_document(self):
        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )

        return document

    def get_queryset(self):
        return self.get_smart_link().get_linked_document_for(
            document=self.get_document()
        )

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                    'smart_link': self.get_smart_link()
                }
            )

        return context

    def get_smart_link(self):
        smart_link = get_object_or_404(
            klass=SmartLink.objects.get_for(document=self.get_document()),
            pk=self.kwargs['smart_link_id']
        )

        AccessControlList.objects.check_access(
            obj=smart_link, permissions=(permission_smart_link_view,),
            user=self.request.user
        )

        return smart_link


class APIResolvedSmartLinkView(generics.RetrieveAPIView):
    """
    get: Return the details of the selected resolved smart link.
    """
    lookup_url_kwarg = 'smart_link_id'
    mayan_object_permissions = {'GET': (permission_smart_link_view,)}
    serializer_class = ResolvedSmartLinkSerializer

    def get_document(self):
        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )

        return document

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document()
                }
            )

        return context

    def get_queryset(self):
        return SmartLink.objects.get_for(document=self.get_document())


class APIResolvedSmartLinkListView(generics.ListAPIView):
    """
    get: Returns a list of the smart links that apply to the document.
    """
    mayan_object_permissions = {'GET': (permission_smart_link_view,)}
    serializer_class = ResolvedSmartLinkSerializer

    def get_document(self):
        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_document_view,),
            user=self.request.user
        )

        return document

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document()
                }
            )

        return context

    def get_queryset(self):
        return SmartLink.objects.filter(
            document_types=self.get_document().document_type
        )


class APISmartLinkConditionListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the smart link conditions.
    post: Create a new smart link condition.
    """
    external_object_class = SmartLink
    external_object_pk_url_kwarg = 'smart_link_id'
    mayan_external_object_permissions = {
        'GET': (permission_smart_link_view,),
        'POST': (permission_smart_link_edit,)
    }
    ordering_fields = ('enabled', 'id')
    serializer_class = SmartLinkConditionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.external_object.conditions.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'smart_link': self.external_object
                }
            )

        return context


class APISmartLinkConditionView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected smart link condition.
    get: Return the details of the selected smart link condition.
    patch: Edit the selected smart link condition.
    put: Edit the selected smart link condition.
    """
    external_object_class = SmartLink
    external_object_pk_url_kwarg = 'smart_link_id'
    lookup_url_kwarg = 'smart_link_condition_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_smart_link_edit,),
        'GET': (permission_smart_link_view,),
        'PATCH': (permission_smart_link_edit,),
        'PUT': (permission_smart_link_edit,)
    }
    serializer_class = SmartLinkConditionSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_queryset(self):
        return self.external_object.conditions.all()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'smart_link': self.external_object
                }
            )

        return context


class APISmartLinkListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the smart links.
    post: Create a new smart link.
    """
    mayan_object_permissions = {'GET': (permission_smart_link_view,)}
    mayan_view_permissions = {'POST': (permission_smart_link_create,)}
    queryset = SmartLink.objects.all()
    serializer_class = SmartLinkSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APISmartLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected smart link.
    get: Return the details of the selected smart link.
    patch: Edit the selected smart link.
    put: Edit the selected smart link.
    """
    lookup_url_kwarg = 'smart_link_id'
    mayan_object_permissions = {
        'DELETE': (permission_smart_link_delete,),
        'GET': (permission_smart_link_view,),
        'PATCH': (permission_smart_link_edit,),
        'PUT': (permission_smart_link_edit,)
    }
    ordering_fields = ('dynamic_label', 'enabled', 'id', 'label')
    queryset = SmartLink.objects.all()
    serializer_class = SmartLinkSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class APISmartLinkDocumentTypeAddView(generics.ObjectActionAPIView):
    """
    post: Add a document type to a smart link.
    """
    lookup_url_kwarg = 'smart_link_id'
    mayan_object_permissions = {
        'POST': (permission_smart_link_edit,)
    }
    serializer_class = SmartLinkDocumentTypeAddSerializer
    queryset = SmartLink.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type']
        self.object._event_actor = self.request.user
        self.object.document_types_add(
            queryset=DocumentType.objects.filter(pk=document_type.pk)
        )


class APISmartLinkDocumentTypeListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Return a list of the selected smart link document types.
    """
    external_object_class = SmartLink
    external_object_pk_url_kwarg = 'smart_link_id'
    mayan_external_object_permissions = {'GET': (permission_smart_link_view,)}
    mayan_object_permissions = {'GET': (permission_document_type_view,)}
    serializer_class = DocumentTypeSerializer

    def get_queryset(self):
        return self.external_object.document_types.all()


class APISmartLinkDocumentTypeRemoveView(generics.ObjectActionAPIView):
    """
    post: Remove a document type from a smart link.
    """
    lookup_url_kwarg = 'smart_link_id'
    mayan_object_permissions = {
        'POST': (permission_smart_link_edit,)
    }
    serializer_class = SmartLinkDocumentTypeRemoveSerializer
    queryset = SmartLink.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type']
        self.object._event_actor = self.request.user
        self.object.document_types_remove(
            queryset=DocumentType.objects.filter(pk=document_type.pk)
        )
