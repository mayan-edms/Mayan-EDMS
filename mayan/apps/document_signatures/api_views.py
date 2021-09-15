from mayan.apps.documents.api_views.mixins import ParentObjectDocumentFileAPIViewMixin
from mayan.apps.rest_api import generics

from .models import DetachedSignature, EmbeddedSignature
from .permissions import (
    permission_document_file_sign_detached,
    permission_document_file_sign_embedded,
    permission_document_file_signature_delete,
    permission_document_file_signature_upload,
    permission_document_file_signature_view
)
from .serializers import (
    DetachedSignatureSerializer, DetachedSignatureUploadSerializer,
    EmbeddedSignatureSerializer, SignDetachedSerializer,
    SignEmbeddedSerializer
)


class APIDocumentFileSignDetachedView(
    ParentObjectDocumentFileAPIViewMixin, generics.ObjectActionAPIView
):
    """
    post: Sign a document file with a detached signature.
    """
    mayan_external_object_permissions = {
        'POST': (permission_document_file_sign_detached,)
    }
    lookup_url_kwarg = 'document_file_id'
    serializer_class = SignDetachedSerializer

    def get_queryset(self):
        return self.get_document_file_queryset()

    def object_action(self, request, serializer):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        DetachedSignature.objects.sign_document_file(
            document_file=self.get_document_file(),
            key=serializer.validated_data['key'],
            passphrase=serializer.validated_data['passphrase'],
            user=self.request.user
        )


class APIDocumentFileSignEmbeddedView(
    ParentObjectDocumentFileAPIViewMixin, generics.ObjectActionAPIView
):
    """
    post: Sign a document file with an embedded signature.
    """
    mayan_external_object_permissions = {
        'POST': (permission_document_file_sign_embedded,)
    }
    lookup_url_kwarg = 'document_file_id'
    serializer_class = SignEmbeddedSerializer

    def get_queryset(self):
        return self.get_document_file_queryset()

    def object_action(self, request, serializer):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        EmbeddedSignature.objects.sign_document_file(
            document_file=self.get_document_file(),
            key=serializer.validated_data['key'],
            passphrase=serializer.validated_data['passphrase'],
            user=self.request.user
        )


class APIDocumentFileDetachedSignatureListView(
    ParentObjectDocumentFileAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the detached signatures of a document file.
    post: Create a detached signature for a document file.
    """
    mayan_external_object_permissions = {
        'GET': (permission_document_file_signature_view,)
    }
    serializer_class = DetachedSignatureSerializer

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_file=self.get_document_file()
        )


class APIDocumentFileDetachedSignatureDetailView(
    ParentObjectDocumentFileAPIViewMixin, generics.RetrieveDestroyAPIView
):
    """
    delete: Delete an detached signature of the selected document.
    get: Returns the details of the selected detached signature.
    """
    mayan_external_object_permissions = {
        'DELETE': (permission_document_file_signature_delete,),
        'GET': (permission_document_file_signature_view,),
        'POST': (permission_document_file_signature_view)
    }
    lookup_url_kwarg = 'detached_signature_id'
    serializer_class = DetachedSignatureSerializer

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_file=self.get_document_file()
        )


class APIDocumentFileDetachedSignatureUploadView(
    ParentObjectDocumentFileAPIViewMixin, generics.CreateAPIView
):
    """
    post: Upload a detached signature file for a document file.
    """
    mayan_external_object_permissions = {
        'POST': (permission_document_file_signature_upload,)
    }
    lookup_url_kwarg = 'document_file_id'
    serializer_class = DetachedSignatureUploadSerializer

    def get_queryset(self):
        return self.get_document_file_queryset()

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document_file': self.get_document_file()
        }


class APIDocumentFileEmbeddedSignatureListView(
    ParentObjectDocumentFileAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the embedded signatures of a document file.
    """
    serializer_class = EmbeddedSignatureSerializer
    mayan_external_object_permissions = {
        'GET': (permission_document_file_signature_view,)
    }

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_file=self.get_document_file()
        )


class APIDocumentFileEmbeddedSignatureDetailView(
    ParentObjectDocumentFileAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns the details of the selected embedded signature.
    """
    mayan_external_object_permissions = {
        'GET': (permission_document_file_signature_view,)
    }
    lookup_url_kwarg = 'embedded_signature_id'
    serializer_class = EmbeddedSignatureSerializer

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_file=self.get_document_file()
        )
