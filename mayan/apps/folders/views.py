from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.views import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)
from documents.permissions import permission_document_view
from documents.models import Document
from documents.views import DocumentListView
from permissions import Permission

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
    post_action_redirect = reverse_lazy('folders:folder_list')
    view_permission = permission_folder_create

    def form_valid(self, form):
        try:
            Folder.on_organization.get(label=form.cleaned_data['label'])
        except Folder.DoesNotExist:
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            return super(FolderCreateView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                _(
                    'A folder named: %s, already exists.'
                ) % form.cleaned_data['label']
            )
            return super(FolderCreateView, self).form_invalid(form)

    def get_extra_context(self):
        return {
            'title': _('Create folder'),
        }

    def get_queryset(self):
        return Folder.on_organization.all()


class FolderDeleteView(SingleObjectDeleteView):
    model = Folder
    object_permission = permission_folder_delete
    post_action_redirect = reverse_lazy('folders:folder_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the folder: %s?') % self.get_object(),
        }

    def get_queryset(self):
        return Folder.on_organization.all()


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
        return get_object_or_404(Folder.on_organization, pk=self.kwargs['pk'])


class FolderEditView(SingleObjectEditView):
    fields = ('label',)
    object_permission = permission_folder_edit
    post_action_redirect = reverse_lazy('folders:folder_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit folder: %s') % self.get_object(),
        }

    def get_queryset(self):
        return Folder.on_organization.all()


class FolderListView(SingleObjectListView):
    object_permission = permission_folder_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Folders'),
        }

    def get_folder_queryset(self):
        return Folder.on_organization.all()

    def get_queryset(self):
        self.queryset = self.get_folder_queryset()
        return super(FolderListView, self).get_queryset()


class DocumentFolderListView(FolderListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(
            Document.on_organization, pk=self.kwargs['pk']
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.document
            )

        return super(DocumentFolderListView, self).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.document,
            'title': _('Folders containing document: %s') % self.document,
        }

    def get_queryset(self):
        return self.document.document_folders().all()


def folder_add_document(request, document_id=None, document_id_list=None):
    queryset = Document.on_organization.all()

    if document_id:
        queryset = queryset.filter(pk=document_id)
    elif document_id_list:
        queryset = queryset.filter(pk__in=document_id_list)

    if not queryset:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    try:
        Permission.check_permissions(
            request.user, (permission_folder_add_document,)
        )
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(
            permission_folder_add_document, request.user, queryset
        )

    post_action_redirect = None
    if document_id:
        post_action_redirect = reverse(
            'folders:document_folder_list', args=(document_id,)
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = FolderListForm(request.POST, user=request.user)
        if form.is_valid():
            folder = form.cleaned_data['folder']
            for document in queryset:
                if document.pk not in folder.documents.values_list('pk', flat=True):
                    folder.documents.add(document)
                    messages.success(
                        request, _(
                            'Document: %(document)s added to folder: '
                            '%(folder)s successfully.'
                        ) % {
                            'document': document, 'folder': folder
                        }
                    )
                else:
                    messages.warning(
                        request, _(
                            'Document: %(document)s is already in '
                            'folder: %(folder)s.'
                        ) % {
                            'document': document, 'folder': folder
                        }
                    )

            return HttpResponseRedirect(next)
    else:
        form = FolderListForm(user=request.user)

    context = {
        'form': form,
        'previous': previous,
        'next': next,
    }

    if queryset.count() == 1:
        context['object'] = queryset.first()

    context['title'] = ungettext(
        'Add document to folder',
        'Add documents to folder',
        queryset.count()
    )

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def folder_document_remove(request, folder_id, document_id=None, document_id_list=None):
    post_action_redirect = None

    folder = get_object_or_404(Folder.on_organization, pk=folder_id)

    if document_id:
        queryset = Document.on_organization.filter(pk=document_id)
    elif document_id_list:
        queryset = Document.on_organization.filter(pk__in=document_id_list)

    if not queryset:
        messages.error(request, _('Must provide at least one folder document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(
            request.user, (permission_folder_remove_document,)
        )
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(
            permission_folder_remove_document, request.user, queryset
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for folder_document in queryset:
            try:
                folder.documents.remove(folder_document)
                messages.success(
                    request, _(
                        'Document: %s removed successfully.'
                    ) % folder_document
                )
            except Exception as exception:
                messages.error(
                    request, _(
                        'Document: %(document)s delete error: %(error)s'
                    ) % {
                        'document': folder_document, 'error': exception
                    }
                )

        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'object': folder,
        'previous': previous,
        'title': ungettext(
            'Remove the selected document from the folder: %(folder)s?',
            'Remove the selected documents from the folder: %(folder)s?',
            queryset.count()
        ) % {'folder': folder}
    }

    if queryset.count() == 1:
        context['object'] = queryset.first()

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def folder_document_multiple_remove(request, folder_id):
    return folder_document_remove(
        request, folder_id, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def folder_add_multiple_documents(request):
    return folder_add_document(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )
