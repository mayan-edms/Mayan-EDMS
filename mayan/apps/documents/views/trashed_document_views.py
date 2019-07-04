from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    ConfirmView, MultipleObjectConfirmActionView
)
from mayan.apps.common.settings import setting_home_view

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
    'DocumentTrashView', 'EmptyTrashCanView', 'TrashedDocumentDeleteView',
    'TrashedDocumentListView', 'TrashedDocumentRestoreView'
)
logger = logging.getLogger(__name__)


class DocumentTrashView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_document_trash
    pk_url_kwarg = 'pk'
    post_action_redirect = reverse_lazy(viewname=setting_home_view.value)
    success_message_singular = _(
        '%(count)d document moved to the trash.'
    )
    success_message_plural = _(
        '%(count)d documents moved to the trash.'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Move the selected document to the trash?',
                plural='Move the selected documents to the trash?',
                number=queryset.count()
            )
        }

        return result

    def object_action(self, form, instance):
        instance.delete()


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
                kwargs={'trashed_document_id': deleted_document.pk}
            )

        messages.success(
            message=_('Trash emptied successfully'), request=self.request
        )


class TrashedDocumentDeleteView(MultipleObjectConfirmActionView):
    model = DeletedDocument
    object_permission = permission_document_delete
    pk_url_kwarg = 'pk'
    success_message_singular = _(
        '%(count)d trashed document deleted.'
    )
    success_message_plural = _(
        '%(count)d trashed documents deleted.'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Delete the selected trashed document?',
                plural='Delete the selected trashed documents?',
                number=queryset.count()
            )
        }

        return result

    def object_action(self, form, instance):
        task_delete_document.apply_async(
            kwargs={'trashed_document_id': instance.pk}
        )


class TrashedDocumentListView(DocumentListView):
    object_permission = None

    def get_document_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view,
            queryset=DeletedDocument.trash.all(),
            user=self.request.user
        )

    def get_extra_context(self):
        context = super(TrashedDocumentListView, self).get_extra_context()
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


class TrashedDocumentRestoreView(MultipleObjectConfirmActionView):
    model = DeletedDocument
    object_permission = permission_document_restore
    pk_url_kwarg = 'pk'
    success_message_singular = _(
        '%(count)d trashed document restored.'
    )
    success_message_plural = _(
        '%(count)d trashed documents restored.'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Restore the selected trashed document?',
                plural='Restore the selected trashed documents?',
                number=queryset.count()
            )
        }

        return result

    def object_action(self, form, instance):
        instance.restore()
