from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.generics import (
    ConfirmView, SingleObjectEditView, SingleObjectListView
)
from common.mixins import MultipleInstanceActionMixin
from documents.models import Document, DocumentType, DocumentVersion
from permissions import Permission

from .forms import DocumentContentForm
from .models import DocumentVersionOCRError
from .permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_ocr_document_delete, permission_document_type_ocr_setup
)


class DocumentAllSubmitView(ConfirmView):
    extra_context = {'title': _('Submit all documents for OCR?')}

    def get_post_action_redirect(self):
        return reverse('common:tools_list')

    def view_action(self):
        count = 0
        for document in Document.objects.all():
            document.submit_for_ocr()
            count += 1

        messages.success(
            self.request, _('%d documents added to the OCR queue.') % count
        )


class DocumentSubmitView(ConfirmView):
    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Submit "%s" to the OCR queue?') % self.get_object()
        }

    def get_object(self):
        return Document.objects.get(pk=self.kwargs['pk'])

    def object_action(self, instance):
        try:
            Permission.check_permissions(
                self.request.user, (permission_ocr_document,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_ocr_document, self.request.user, instance
            )

        instance.submit_for_ocr()

    def view_action(self):
        instance = self.get_object()

        self.object_action(instance=instance)

        messages.success(
            self.request,
            _('Document: %(document)s was added to the OCR queue.') % {
                'document': instance
            }
        )


class DocumentSubmitManyView(MultipleInstanceActionMixin, DocumentSubmitView):
    model = Document
    success_message = '%(count)d document submitted to the OCR queue.'
    success_message_plural = '%(count)d documents submitted to the OCR queue.'

    def get_extra_context(self):
        # Override the base class method
        return {
            'title': _('Submit the selected documents to the OCR queue?')
        }


class DocumentTypeSettingsEditView(SingleObjectEditView):
    fields = ('auto_ocr',)
    view_permission = permission_document_type_ocr_setup

    def get_object(self, queryset=None):
        return get_object_or_404(
            DocumentType, pk=self.kwargs['pk']
        ).ocr_settings

    def get_extra_context(self):
        return {
            'title': _(
                'Edit OCR settings for document type: %s'
            ) % self.get_object().document_type
        }


def document_content(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.check_permissions(
            request.user, (permission_ocr_content_view,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_ocr_content_view, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    content_form = DocumentContentForm(document=document)

    return render_to_response('appearance/generic_form.html', {
        'document': document,
        'form': content_form,
        'hide_labels': True,
        'object': document,
        'read_only': True,
        'title': _('Content of document: %s') % document,
    }, context_instance=RequestContext(request))


class EntryListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('OCR errors'),
    }
    view_permission = permission_ocr_document

    def get_queryset(self):
        return DocumentVersionOCRError.objects.all()


def entry_delete(request, pk=None, pk_list=None):
    Permission.check_permissions(
        request.user, (permission_ocr_document_delete,)
    )

    if pk:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk)]
    elif pk_list:
        entries = [
            get_object_or_404(
                DocumentVersionOCRError, pk=pk
            ) for pk in pk_list.split(',')
        ]
    else:
        messages.error(request, _('Make at least one selection.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for entry in entries:
            try:
                entry.delete()
                messages.success(
                    request, _('Entry: %(entry)s deleted successfully.') % {
                        'entry': entry
                    }
                )

            except Exception as exception:
                messages.error(
                    request, _('Error entry: %(entry)s; %(error)s') % {
                        'entry': entry, 'error': exception
                    }
                )
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'delete_view': True,
    }

    if len(entries) == 1:
        context['object'] = entries[0]

    context['title'] = ungettext(
        'Delete the selected entry?',
        'Delete the selected entries?',
        len(entries)
    )

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def entry_delete_multiple(request):
    return entry_delete(request, pk_list=request.GET.get('id_list', ''))


def entry_re_queue(request, pk=None, pk_list=None):
    Permission.check_permissions(request.user, (permission_ocr_document,))

    if pk:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk)]
    elif pk_list:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk) for pk in pk_list.split(',')]
    else:
        messages.error(request, _('Make at least one selection.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for entry in entries:
            try:
                entry.document_version.submit_for_ocr()
                messages.success(
                    request,
                    _('Entry: %(entry)s was re-queued for OCR.') % {
                        'entry': entry
                    }
                )
            except DocumentVersion.DoesNotExist:
                messages.error(
                    request, _(
                        'Document version id#: %d, no longer exists.'
                    ) % entry.document_version_id
                )
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
    }

    if len(entries) == 1:
        context['object'] = entries[0]

    context['title'] = ungettext(
        'Re-queue the selected entry?',
        'Re-queue the selected entries?',
        len(entries)
    )

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def entry_re_queue_multiple(request):
    return entry_re_queue(request, pk_list=request.GET.get('id_list', []))
