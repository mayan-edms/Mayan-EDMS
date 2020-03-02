from __future__ import absolute_import, unicode_literals

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from mayan.apps.documents.models import Document
from mayan.apps.documents.serializers import DocumentSerializer
from mayan.apps.rest_api import viewsets

from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)
from .serializers import (
    DocumentTagAttachRemoveSerializer,
    TagDocumentAttachRemoveSerializer, TagSerializer
)


class DocumentTagAPIViewSet(viewsets.MayanGenericAPIViewSet):
    lookup_url_kwarg = 'document_id'
    object_permission_map = {
        'tag_attach': permission_tag_attach,
        'tag_list': permission_tag_view,
        'tag_remove': permission_tag_remove,
    }
    queryset = Document.objects.all()

    @action(
        detail=True, lookup_url_kwarg='document_id', methods=('post',),
        serializer_class=DocumentTagAttachRemoveSerializer,
        url_name='tag-attach', url_path='tags/attach'
    )
    def tag_attach(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.tag_attach(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @action(
        detail=True, lookup_url_kwarg='document_id',
        serializer_class=TagSerializer, url_name='tag-list',
        url_path='tags'
    )
    def tag_list(self, request, *args, **kwargs):
        queryset = self.get_object().get_tags(
            permission=permission_tag_view, user=self.request.user
        )
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @action(
        detail=True, lookup_url_kwarg='document_id', methods=('post',),
        serializer_class=DocumentTagAttachRemoveSerializer,
        url_name='tag-remove', url_path='tags/remove'
    )
    def tag_remove(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.tag_remove(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class TagAPIViewSet(viewsets.MayanModelAPIViewSet):
    lookup_url_kwarg = 'tag_id'
    object_permission_map = {
        'destroy': permission_tag_delete,
        'document_attach': permission_tag_attach,
        'document_list': permission_tag_view,
        'document_remove': permission_tag_remove,
        'list': permission_tag_view,
        'partial_update': permission_tag_edit,
        'retrieve': permission_tag_view,
        'update': permission_tag_edit
    }
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    view_permission_map = {
        'create': permission_tag_create
    }

    @action(
        detail=True, lookup_url_kwarg='tag_id', methods=('post',),
        serializer_class=TagDocumentAttachRemoveSerializer,
        url_name='document-attach', url_path='documents/attach'
    )
    def document_attach(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.document_attach(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    @action(
        detail=True, lookup_url_kwarg='tag_id', methods=('get',),
        serializer_class=DocumentSerializer, url_name='document-list',
        url_path='documents'
    )
    def document_list(self, request, *args, **kwargs):
        queryset = self.get_object().get_documents(user=self.request.user)
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @action(
        detail=True, lookup_url_kwarg='tag_id', methods=('post',),
        serializer_class=TagDocumentAttachRemoveSerializer,
        url_name='document-remove', url_path='documents/remove'
    )
    def document_remove(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.document_remove(instance=instance)
        headers = self.get_success_headers(data=serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )
