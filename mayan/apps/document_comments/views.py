from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectListView
)
from documents.models import Document
from permissions import Permission

from .models import Comment
from .permissions import (
    permission_comment_create, permission_comment_delete,
    permission_comment_view
)


class DocumentCommentCreateView(SingleObjectCreateView):
    fields = ('comment',)
    model = Comment
    object_verbose_name = _('Comment')

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_comment_create,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_comment_create, request.user, self.get_document()
            )

        return super(
            DocumentCommentCreateView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'object': self.get_document(),
            'title': _('Add comment to document: %s') % self.get_document(),
        }

    def get_instance_extra_data(self):
        return {
            'document': self.get_document(), 'user': self.request.user,
        }

    def get_save_extra_data(self):
        return {
            '_user': self.request.user,
        }

    def get_post_action_redirect(self):
        return reverse(
            'comments:comments_for_document', args=(self.kwargs['pk'],)
        )


class DocumentCommentDeleteView(SingleObjectDeleteView):
    model = Comment

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_comment_delete,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_comment_delete, request.user,
                self.get_object().document
            )

        return super(
            DocumentCommentDeleteView, self
        ).dispatch(request, *args, **kwargs)

    def get_delete_extra_data(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.get_object().document,
            'title': _('Delete comment: %s?') % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            'comments:comments_for_document',
            args=(self.get_object().document.pk,)
        )


class DocumentCommentListView(SingleObjectListView):
    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        try:
            Permission.check_permissions(
                self.request.user, (permission_comment_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_comment_view, self.request.user,
                self.get_document()
            )

        return self.get_document().comments.all()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'object': self.get_document(),
            'title': _('Comments for document: %s') % self.get_document(),
        }
