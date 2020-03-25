from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.rest_api import generics

from .models import DetachedSignature, EmbeddedSignature
from .permissions import (
    permission_document_version_sign_detached,
    permission_document_version_sign_embedded,
    permission_document_version_signature_delete,
    permission_document_version_signature_upload,
    permission_document_version_signature_view
)
from .serializers import (
    DetachedSignatureSerializer, EmbeddedSignatureSerializer,
    SignDetachedSerializer, SignEmbeddedSerializer
)


class APIDocumentSignDetachedView(generics.GenericAPIView):
    """
    post: Sign a document version with a detached signature.
    """
    serializer_class = SignDetachedSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'POST':
            permission = permission_document_version_sign_detached

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(
            APIDocumentSignDetachedView, self
        ).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(
            APIDocumentSignDetachedView, self
        ).get_serializer_context()

        if self.kwargs:
            context.update(
                {
                    'document_version': self.get_document_version(),
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
    post: Sign a document version with an embedded signature.
    """
    serializer_class = SignEmbeddedSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'POST':
            permission = permission_document_version_sign_embedded

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(
            APIDocumentSignEmbeddedView, self
        ).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(
            APIDocumentSignEmbeddedView, self
        ).get_serializer_context()

        if self.kwargs:
            context.update(
                {
                    'document_version': self.get_document_version(),
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
    get: Returns a list of all the detached signatures of a document version.
    post: Create an detached signature for a document version.
    """
    serializer_class = DetachedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_version_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_version_signature_upload

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(
            APIDocumentDetachedSignatureListView, self
        ).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(
            APIDocumentDetachedSignatureListView, self
        ).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document_version': self.get_document_version(),
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
            permission = permission_document_version_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_version_signature_view
        elif self.request.method == 'DELETE':
            permission = permission_document_version_signature_delete

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return DetachedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentDetachedSignatureView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context


class APIDocumentEmbeddedSignatureListView(generics.ListAPIView):
    """
    get: Returns a list of all the embedded signatures of a document version.
    """
    serializer_class = EmbeddedSignatureSerializer

    def get_document(self):
        return get_object_or_404(
            klass=self.get_document_queryset(), pk=self.kwargs['document_id']
        )

    def get_document_queryset(self):
        if self.request.method == 'GET':
            permission = permission_document_version_signature_view

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(
            APIDocumentEmbeddedSignatureListView, self
        ).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(
            APIDocumentEmbeddedSignatureListView, self
        ).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document_version': self.get_document_version(),
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
            permission = permission_document_version_signature_view
        elif self.request.method == 'POST':
            permission = permission_document_version_signature_view

        return AccessControlList.objects.restrict_queryset(
            permission=permission, queryset=Document.objects.all(),
            user=self.request.user
        )

    def get_document_version(self):
        return get_object_or_404(
            klass=self.get_document_version_queryset(),
            pk=self.kwargs['document_version_id']
        )

    def get_document_version_queryset(self):
        return self.get_document().versions.all()

    def get_queryset(self):
        return EmbeddedSignature.objects.filter(
            document_version=self.get_document_version()
        )

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentEmbeddedSignatureView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context
