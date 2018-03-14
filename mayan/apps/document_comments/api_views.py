from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from rest_framework import generics

from acls.models import AccessControlList
from documents.models import Document

from .permissions import (
    permission_comment_create, permission_comment_delete,
    permission_comment_view
)
from .serializers import CommentSerializer, WritableCommentSerializer


class APICommentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the document comments.
    post: Create a new document comment.
    """
    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_comment_view
        else:
            permission_required = permission_comment_create

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])

        AccessControlList.objects.check_access(
            permissions=permission_required, user=self.request.user,
            obj=document
        )

        return document

    def get_queryset(self):
        return self.get_document().comments.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super(APICommentListView, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        else:
            return WritableCommentSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        context = super(APICommentListView, self).get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'document': self.get_document(),
                }
            )

        return context


class APICommentView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete the selected document comment.
    get: Returns the details of the selected document comment.
    """
    lookup_url_kwarg = 'comment_pk'
    serializer_class = CommentSerializer

    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_comment_view
        else:
            permission_required = permission_comment_delete

        document = get_object_or_404(Document, pk=self.kwargs['document_pk'])

        AccessControlList.objects.check_access(
            permissions=permission_required, user=self.request.user,
            obj=document
        )

        return document

    def get_queryset(self):
        return self.get_document().comments.all()
