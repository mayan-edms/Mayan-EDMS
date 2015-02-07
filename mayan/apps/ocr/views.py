from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessEntry
from documents.models import Document, DocumentVersion
from permissions.models import Permission

from .api import clean_pages
from .models import DocumentVersionOCRError
from .permissions import (
    PERMISSION_OCR_CLEAN_ALL_PAGES, PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE
)


def document_submit(request, pk):
    document = get_object_or_404(Document, pk=pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_OCR_DOCUMENT, request.user, document)

    document.submit_for_ocr()
    messages.success(request, _('Document: %(document)s was added to the OCR queue.') % {
        'document': document}
    )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))


def document_submit_multiple(request):
    for item_id in request.GET.get('id_list', '').split(','):
        document_submit(request, item_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))


def document_all_ocr_cleanup(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_CLEAN_ALL_PAGES])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('main/generic_confirm.html', {
            'previous': previous,
            'next': next,
            'title': _('Are you sure you wish to clean up all the pages content?'),
            'message': _('On large databases this operation may take some time to execute.'),
        }, context_instance=RequestContext(request))
    else:
        try:
            # TODO: turn this into a Celery task
            clean_pages()
            messages.success(request, _('Document pages content clean up complete.'))
        except Exception as exception:
            messages.error(request, _('Document pages content clean up error: %s') % exception)

        return HttpResponseRedirect(next)


def entry_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])

    context = {
        'object_list': DocumentVersionOCRError.objects.all(),
        'title': _('OCR errors'),
        'hide_object': True,
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def entry_delete(request, pk=None, pk_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT_DELETE])

    if pk:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk)]
    elif pk_list:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk) for pk in pk_list.split(',')]
    else:
        messages.error(request, _('Make at least one selection.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        for entry in entries:
            try:
                entry.delete()
                messages.success(request, _('Entry: %(entry)s deleted successfully.') % {
                    'entry': entry})

            except Exception as exception:
                messages.error(request, _('Error entry: %(entry)s; %(error)s') % {
                    'entry': entry, 'error': exception})
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'delete_view': True,
    }

    if len(entries) == 1:
        context['object'] = entries[0]

    context['title'] = ungettext(
        'Are you sure you wish to delete the selected entry?',
        'Are you sure you wish to delete the selected entries?',
        len(entries)
    )

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def entry_delete_multiple(request):
    return entry_delete(request, pk_list=request.GET.get('id_list', ''))


def entry_re_queue(request, pk=None, pk_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])

    if pk:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk)]
    elif pk_list:
        entries = [get_object_or_404(DocumentVersionOCRError, pk=pk) for pk in pk_list.split(',')]
    else:
        messages.error(request, _('Make at least one selection.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

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
                messages.error(request, _('Document version id#: %d, no longer exists.') % entry.document_version_id)
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
    }

    if len(entries) == 1:
        context['object'] = entries[0]

    context['title'] = ungettext(
        'Are you sure you wish to re-queue the selected entry?',
        'Are you sure you wish to re-queue the selected entries?',
        len(entries)
    )

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def entry_re_queue_multiple(request):
    return entry_re_queue(request, pk_list=request.GET.get('id_list', []))
