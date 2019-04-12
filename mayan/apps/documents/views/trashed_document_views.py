from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import ConfirmView
from mayan.apps.common.mixins import MultipleInstanceActionMixin

from ..icons import icon_document_list_deleted
from ..models import DeletedDocument, Document
from ..permissions import (
    permission_document_delete, permission_document_restore,
    permission_document_trash, permission_document_view,
    permission_empty_trash
)
from ..tasks import task_delete_document

from .document_views import DocumentListView

__all__ = (
    'DeletedDocumentDeleteView', 'DeletedDocumentDeleteManyView',
    'DeletedDocumentListView', 'DocumentRestoreView', 'DocumentRestoreManyView',
    'DocumentTrashView', 'DocumentTrashManyView', 'EmptyTrashCanView'
)
logger = logging.getLogger(__name__)


class DeletedDocumentDeleteView(ConfirmView):
    extra_context = {
        'title': _('Delete the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            klass=Document.passthrough, pk=instance.pk
        )

        AccessControlList.objects.check_access(
            permissions=permission_document_delete, user=self.request.user,
            obj=source_document
        )

        task_delete_document.apply_async(
            kwargs={'deleted_document_id': instance.pk}
        )

    def view_action(self):
        instance = get_object_or_404(
            klass=DeletedDocument, pk=self.kwargs['pk']
        )
        self.object_action(instance=instance)
        messages.success(
            self.request, _('Document: %(document)s deleted.') % {
                'document': instance
            }
        )


class DeletedDocumentDeleteManyView(MultipleInstanceActionMixin, DeletedDocumentDeleteView):
    extra_context = {
        'title': _('Delete the selected documents?')
    }
    model = DeletedDocument
    success_message = '%(count)d document deleted.'
    success_message_plural = '%(count)d documents deleted.'


class DeletedDocumentListView(DocumentListView):
    object_permission = None

    def get_document_queryset(self):
        return AccessControlList.objects.filter_by_access(
            permission_document_view, self.request.user,
            queryset=DeletedDocument.trash.all()
        )

    def get_extra_context(self):
        context = super(DeletedDocumentListView, self).get_extra_context()
        context.update(
            {
                'hide_link': True,
                'no_results_icon': icon_document_list_deleted,
                'no_results_text': _(
                    'To avoid loss of data, documents are not deleted '
                    'instantly. First, they are placed in the trash can. '
                    'From here they can be then finally deleted or restored.'
                ),
                'no_results_title': _(
                    'There are no documents in the trash can'
                ),
                'title': _('Documents in trash'),
            }
        )
        return context


class DocumentRestoreView(ConfirmView):
    extra_context = {
        'title': _('Restore the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            klass=Document.passthrough, pk=instance.pk
        )

        AccessControlList.objects.check_access(
            permissions=permission_document_restore, user=self.request.user,
            obj=source_document
        )

        instance.restore()

    def view_action(self):
        instance = get_object_or_404(
            klass=DeletedDocument, pk=self.kwargs['pk']
        )

        self.object_action(instance=instance)

        messages.success(
            self.request, _('Document: %(document)s restored.') % {
                'document': instance
            }
        )


class DocumentRestoreManyView(MultipleInstanceActionMixin, DocumentRestoreView):
    extra_context = {
        'title': _('Restore the selected documents?')
    }
    model = DeletedDocument
    success_message = '%(count)d document restored.'
    success_message_plural = '%(count)d documents restored.'


class DocumentTrashView(ConfirmView):
    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Move "%s" to the trash?') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse('documents:document_list_recent_access')

    def object_action(self, instance):
        AccessControlList.objects.check_access(
            permissions=permission_document_trash, user=self.request.user,
            obj=instance
        )

        instance.delete()

    def view_action(self):
        instance = self.get_object()

        self.object_action(instance=instance)

        messages.success(
            self.request, _('Document: %(document)s moved to trash successfully.') % {
                'document': instance
            }
        )


class DocumentTrashManyView(MultipleInstanceActionMixin, DocumentTrashView):
    model = Document
    success_message = '%(count)d document moved to the trash.'
    success_message_plural = '%(count)d documents moved to the trash.'

    def get_extra_context(self):
        return {
            'title': _('Move the selected documents to the trash?')
        }


class EmptyTrashCanView(ConfirmView):
    extra_context = {
        'title': _('Empty trash?')
    }
    view_permission = permission_empty_trash
    action_cancel_redirect = post_action_redirect = reverse_lazy(
        'documents:document_list_deleted'
    )

    def view_action(self):
        for deleted_document in DeletedDocument.objects.all():
            task_delete_document.apply_async(
                kwargs={'deleted_document_id': deleted_document.pk}
            )

        messages.success(self.request, _('Trash emptied successfully'))
