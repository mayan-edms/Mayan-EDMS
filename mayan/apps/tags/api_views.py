from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.serializers import DocumentSerializer
from mayan.apps.rest_api import generics

from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)
from .serializers import (
    DocumentTagSerializer, NewDocumentTagSerializer, TagSerializer,
    WritableTagSerializer
)


class APITagListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the tags.
    post: Create a new tag.
    """
    mayan_object_permissions = {'GET': (permission_tag_view,)}
    mayan_view_permissions = {'POST': (permission_tag_create,)}
    queryset = Tag.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APITagListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagSerializer
        elif self.request.method == 'POST':
            return WritableTagSerializer


class APITagView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected tag.
    get: Return the details of the selected tag.
    patch: Edit the selected tag.
    put: Edit the selected tag.
    """
    mayan_object_permissions = {
        'DELETE': (permission_tag_delete,),
        'GET': (permission_tag_view,),
        'PATCH': (permission_tag_edit,),
        'PUT': (permission_tag_edit,)
    }
    queryset = Tag.objects.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APITagView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagSerializer
        else:
            return WritableTagSerializer


class APITagDocumentListView(generics.ListAPIView):
    """
    get: Returns a list of all the documents tagged by a particular tag.
    """
    mayan_object_permissions = {'GET': (permission_document_view,)}
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=Tag.objects.all(), permission=permission_tag_view,
            user=self.request.user
        )

        tag = get_object_or_404(klass=queryset, pk=self.kwargs['pk'])

        return tag.documents.all()


class APIDocumentTagListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the tags attached to a document.
    post: Attach a tag to a document.
    """
    mayan_object_permissions = {
        'GET': (permission_tag_view,),
        'POST': (permission_tag_attach,)
    }

    def get_document(self):
        if self.request.method == 'GET':
            permission = permission_tag_view
        elif self.request.method == 'POST':
            permission = permission_tag_attach

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=Document.objects.all(), permission=permission,
            user=self.request.user
        )
        return get_object_or_404(
            klass=queryset, pk=self.kwargs['document_pk']
        )

    def get_queryset(self):
        return self.get_document().tags.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTagListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DocumentTagSerializer
        elif self.request.method == 'POST':
            return NewDocumentTagSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentTagListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context

    def perform_create(self, serializer):
        serializer.save(document=self.get_document())


class APIDocumentTagView(generics.RetrieveDestroyAPIView):
    """
    delete: Remove a tag from the selected document.
    get: Returns the details of the selected document tag.
    """
    mayan_object_permissions = {
        'GET': (permission_tag_view,),
        'DELETE': (permission_tag_remove,)
    }
    serializer_class = DocumentTagSerializer

    def get_document(self):
        if self.request.method == 'GET':
            permission = permission_tag_view
        elif self.request.method == 'DELETE':
            permission = permission_tag_remove

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=Document.objects.all(), permission=permission,
            user=self.request.user
        )
        return get_object_or_404(
            klass=queryset, pk=self.kwargs['document_pk']
        )

    def get_queryset(self):
        return self.get_document().tags.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APIDocumentTagView, self).get_serializer(*args, **kwargs)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APIDocumentTagView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context

    def perform_destroy(self, instance):
        try:
            instance.documents.remove(self.get_document())
        except Exception as exception:
            raise ValidationError(exception)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
