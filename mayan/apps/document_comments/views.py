from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import Document
from mayan.apps.views.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from .forms import DocumentCommentDetailForm
from .icons import icon_comments_for_document
from .links import link_comment_add
from .models import Comment
from .permissions import (
    permission_document_comment_create, permission_document_comment_delete,
    permission_document_comment_edit, permission_document_comment_view
)


class DocumentCommentCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = Document
    external_object_permission = permission_document_comment_create
    external_object_pk_url_kwarg = 'document_id'
    fields = ('comment',)

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _('Add comment to document: %s') % self.external_object,
        }

    def get_instance_extra_data(self):
        return {
            'document': self.external_object, 'user': self.request.user,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='comments:comments_for_document', kwargs={
                'document_id': self.kwargs['document_id']
            }
        )

    def get_queryset(self):
        return self.external_object.comments.all()

    def get_save_extra_data(self):
        return {
            '_user': self.request.user,
        }


class DocumentCommentDeleteView(SingleObjectDeleteView):
    model = Comment
    object_permission = permission_document_comment_delete
    pk_url_kwarg = 'comment_id'

    def get_delete_extra_data(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _('Delete comment: %s?') % self.object,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='comments:comments_for_document', kwargs={
                'document_id': self.object.document.pk
            }
        )


class DocumentCommentDetailView(SingleObjectDetailView):
    form_class = DocumentCommentDetailForm
    model = Comment
    pk_url_kwarg = 'comment_id'
    object_permission = permission_document_comment_view

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _('Details for comment: %s?') % self.object,
        }


class DocumentCommentEditView(SingleObjectEditView):
    fields = ('comment',)
    model = Comment
    pk_url_kwarg = 'comment_id'
    object_permission = permission_document_comment_edit

    def get_save_extra_data(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'comment': self.object,
            'document': self.object.document,
            'navigation_object_list': ('document', 'comment'),
            'title': _('Edit comment: %s?') % self.object,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='comments:comments_for_document', kwargs={
                'document_id': self.object.document.pk
            }
        )


class DocumentCommentListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_document_comment_view
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_comments_for_document,
            'no_results_external_link': link_comment_add.resolve(
                RequestContext(self.request, {'object': self.external_object})
            ),
            'no_results_text': _(
                'Document comments are timestamped text entries from users. '
                'They are great for collaboration.'
            ),
            'no_results_title': _('There are no comments'),
            'object': self.external_object,
            'title': _('Comments for document: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.comments.all()
