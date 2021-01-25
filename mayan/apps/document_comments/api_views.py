from django.shortcuts import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.rest_api import generics

from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)
from .serializers import CommentSerializer, WritableCommentSerializer


class APICommentListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the document comments.
    post: Create a new document comment.
    """
    def get_document(self):
        if self.request.method == 'GET':
            permission_required = permission_document_comment_view
        else:
            permission_required = permission_document_comment_create

        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_required,),
            user=self.request.user
        )

        return document

    def get_queryset(self):
        return self.get_document().comments.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        else:
            return WritableCommentSerializer

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


class APICommentView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected document comment.
    get: Returns the details of the selected document comment.
    """
    lookup_url_kwarg = 'comment_id'
    serializer_class = CommentSerializer

    def get_document(self):
        if self.request.method == 'DELETE':
            permission_required = permission_document_comment_delete
        elif self.request.method in ('PATCH', 'PUT'):
            permission_required = permission_document_comment_edit
        else:
            permission_required = permission_document_comment_view

        document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=document, permissions=(permission_required,),
            user=self.request.user
        )

        return document

    def get_queryset(self):
        return self.get_document().comments.all()

    def perform_destroy(self, instance):
        instance._event_actor = self.request.user
        return super().perform_destroy(instance=instance)

    def perform_update(self, serializer):
        serializer.validated_data['_event_actor'] = self.request.user
        return super().perform_update(serializer=serializer)
