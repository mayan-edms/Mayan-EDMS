from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
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


class APIDocumentSignatureViewMixin:
    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=self._document_view_permissions[self.request.method],
            queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()


class APIDocumentFileSignDetachedView(
    APIDocumentSignatureViewMixin, generics.ObjectActionAPIView
):
    """
    post: Sign a document file with a detached signature.
    """
    _document_view_permissions = {
        'POST': permission_document_file_sign_detached,
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
    APIDocumentSignatureViewMixin, generics.ObjectActionAPIView
):
    """
    post: Sign a document file with an embedded signature.
    """
    _document_view_permissions = {
        'POST': permission_document_file_sign_embedded
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
    APIDocumentSignatureViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the detached signatures of a document file.
    post: Create a detached signature for a document file.
    """
    _document_view_permissions = {
        'GET': permission_document_file_signature_view,
    }
    serializer_class = DetachedSignatureSerializer

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_file=self.get_document_file()
        )

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document_file': self.get_document_file(),
                }
            )

        return context


class APIDocumentFileDetachedSignatureDetailView(
    APIDocumentSignatureViewMixin, generics.RetrieveDestroyAPIView
):
    """
    delete: Delete an detached signature of the selected document.
    get: Returns the details of the selected detached signature.
    """
    _document_view_permissions = {
        'DELETE': permission_document_file_signature_delete,
        'GET': permission_document_file_signature_view,
        'POST': permission_document_file_signature_view
    }
    lookup_url_kwarg = 'detached_signature_id'
    serializer_class = DetachedSignatureSerializer

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_file=self.get_document_file()
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
                }
            )

        return context


class APIDocumentFileDetachedSignatureUploadView(
    APIDocumentSignatureViewMixin, generics.CreateAPIView
):
    """
    post: Upload a detached signature file for a document file.
    """
    _document_view_permissions = {
        'POST': permission_document_file_signature_upload
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
    APIDocumentSignatureViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the embedded signatures of a document file.
    """
    serializer_class = EmbeddedSignatureSerializer
    _document_view_permissions = {
        'GET': permission_document_file_signature_view
    }

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_file=self.get_document_file()
        )

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document_file': self.get_document_file(),
                }
            )

        return context


class APIDocumentFileEmbeddedSignatureDetailView(
    APIDocumentSignatureViewMixin, generics.RetrieveAPIView
):
    """
    get: Returns the details of the selected embedded signature.
    """
    _document_view_permissions = {
        'GET': permission_document_file_signature_view,
    }
    lookup_url_kwarg = 'embedded_signature_id'
    serializer_class = EmbeddedSignatureSerializer

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_file=self.get_document_file()
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
                }
            )

        return context
