from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

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
    DetachedSignatureSerializer, EmbeddedSignatureSerializer,
    SignDetachedSerializer, SignEmbeddedSerializer
)


class APIDocumentSignDetachedView(generics.GenericAPIView):
    """
    post: Sign a document file with a detached signature.
    """
    serializer_class = SignDetachedSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'POST':
            permission = permission_document_file_sign_detached

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.sign(
            key_id=request.data['key_id'],
            passphrase=request.data['passphrase']
        )
        return Response(status=status.HTTP_200_OK)


class APIDocumentSignEmbeddedView(generics.GenericAPIView):
    """
    post: Sign a document file with an embedded signature.
    """
    serializer_class = SignEmbeddedSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'POST':
            permission = permission_document_file_sign_embedded

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.sign(
            key_id=request.data['key_id'],
            passphrase=request.data['passphrase']
        )
        return Response(status=status.HTTP_200_OK)


class APIDocumentDetachedSignatureListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the detached signatures of a document file.
    post: Create a detached signature for a document file.
    """
    serializer_class = DetachedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_file_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_file_signature_upload

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
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


class APIDocumentDetachedSignatureView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete an detached signature of the selected document.
    get: Returns the details of the selected detached signature.
    """
    lookup_url_kwarg = 'detached_signature_id'
    serializer_class = DetachedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_file_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_file_signature_view
        elif self.request.method == 'DELETE':
            permission = permission_document_file_signature_delete

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

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


class APIDocumentEmbeddedSignatureListView(generics.ListAPIView):
    """
    get: Returns a list of all the embedded signatures of a document file.
    """
    serializer_class = EmbeddedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_file_signature_view

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

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


class APIDocumentEmbeddedSignatureView(generics.RetrieveAPIView):
    """
    get: Returns the details of the selected embedded signature.
    """
    lookup_url_kwarg = 'embedded_signature_id'
    serializer_class = EmbeddedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_file_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_file_signature_view

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_file(self):
        return get_object_or_404(
            klass=self.get_document_file_queryset(),
            pk=self.kwargs['document_file_id']
        )

    def get_document_file_queryset(self):
        return self.get_document().files.all()

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
