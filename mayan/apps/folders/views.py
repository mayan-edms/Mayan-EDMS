from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.views import (
    MultipleObjectFormActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from documents.permissions import permission_document_view
from documents.models import Document
from documents.views import DocumentListView

from .forms import FolderListForm
from .models import Folder
from .permissions import (
    permission_folder_add_document, permission_folder_create,
    permission_folder_delete, permission_folder_edit, permission_folder_view,
    permission_folder_remove_document
)

logger = logging.getLogger(__name__)


class FolderCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = Folder
    view_permission = permission_folder_create

    def get_extra_context(self):
        return {
            'title': _('Create folder'),
        }


class FolderDeleteView(SingleObjectDeleteView):
    model = Folder
    object_permission = permission_folder_delete
    post_action_redirect = reverse_lazy('folders:folder_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the folder: %s?') % self.get_object(),
        }


class FolderDetailView(DocumentListView):
    def get_document_queryset(self):
        return self.get_folder().documents.all()

    def get_extra_context(self):
        return {
            'hide_links': True,
            'object': self.get_folder(),
            'title': _('Documents in folder: %s') % self.get_folder(),
        }

    def get_folder(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=permission_folder_view, user=self.request.user,
            obj=folder
        )

        return folder


class FolderEditView(SingleObjectEditView):
    fields = ('label',)
    model = Folder
    object_permission = permission_folder_edit
    post_action_redirect = reverse_lazy('folders:folder_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit folder: %s') % self.get_object(),
        }


class FolderListView(SingleObjectListView):
    model = Folder
    object_permission = permission_folder_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Folders'),
        }


class DocumentFolderListView(FolderListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=request.user,
            obj=self.document
        )

        return super(DocumentFolderListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.document,
            'title': _('Folders containing document: %s') % self.document,
        }

    def get_queryset(self):
        return self.document.document_folders().all()


class DocumentAddToFolderView(MultipleObjectFormActionView):
    form_class = FolderListForm
    model = Document
    success_message = _(
        'Add to folder request performed on %(count)d document'
    )
    success_message_plural = _(
        'Add to folder request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        result = {
            'submit_label': _('Add'),
            'title': ungettext(
                'Add document to folders',
                'Add documents to folders',
                queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Add document "%s" to folders'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.get_queryset()
        result = {
            'help_text': _(
                'Folders to which the selected documents will be added.'
            ),
            'permission': permission_folder_add_document,
            'user': self.request.user
        }

        if queryset.count() == 1:
            result.update(
                {
                    'queryset': Folder.objects.exclude(
                        pk__in=queryset.first().folders.all()
                    )
                }
            )

        return result

    def object_action(self, form, instance):
        folder_membership = instance.folders.all()

        for folder in form.cleaned_data['folders']:
            AccessControlList.objects.check_access(
                obj=folder, permissions=permission_folder_add_document,
                user=self.request.user
            )

            if folder in folder_membership:
                messages.warning(
                    self.request, _(
                        'Document: %(document)s is already in '
                        'folder: %(folder)s.'
                    ) % {
                        'document': instance, 'folder': folder
                    }
                )
            else:
                folder.documents.add(instance)
                messages.success(
                    self.request, _(
                        'Document: %(document)s added to folder: '
                        '%(folder)s successfully.'
                    ) % {
                        'document': instance, 'folder': folder
                    }
                )


class DocumentRemoveFromFolderView(MultipleObjectFormActionView):
    form_class = FolderListForm
    model = Document
    success_message = _(
        'Remove from folder request performed on %(count)d document'
    )
    success_message_plural = _(
        'Remove from folder request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        result = {
            'submit_label': _('Remove'),
            'title': ungettext(
                'Remove document from folders',
                'Remove documents from folders',
                queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Remove document "%s" to folders'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.get_queryset()
        result = {
            'help_text': _(
                'Folders from which the selected documents will be removed.'
            ),
            'permission': permission_folder_remove_document,
            'user': self.request.user
        }

        if queryset.count() == 1:
            result.update(
                {
                    'queryset': queryset.first().folders.all()
                }
            )

        return result

    def object_action(self, form, instance):
        folder_membership = instance.folders.all()

        for folder in form.cleaned_data['folders']:
            AccessControlList.objects.check_access(
                obj=folder, permissions=permission_folder_remove_document,
                user=self.request.user
            )

            if folder not in folder_membership:
                messages.warning(
                    self.request, _(
                        'Document: %(document)s is not in folder: %(folder)s.'
                    ) % {
                        'document': instance, 'folder': folder
                    }
                )
            else:
                folder.documents.remove(instance)
                messages.success(
                    self.request, _(
                        'Document: %(document)s removed from folder: '
                        '%(folder)s.'
                    ) % {
                        'document': instance, 'folder': folder
                    }
                )
