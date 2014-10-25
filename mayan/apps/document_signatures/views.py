from __future__ import absolute_import

from datetime import datetime
import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import force_escape
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from django_gpg.literals import SIGNATURE_STATE_NONE, SIGNATURE_STATES
from documents.models import Document
from filetransfers.api import serve_file
from permissions.models import Permission

from .forms import DetachedSignatureForm
from .models import DocumentVersionSignature
from .permissions import (PERMISSION_DOCUMENT_VERIFY,
                          PERMISSION_SIGNATURE_UPLOAD,
                          PERMISSION_SIGNATURE_DOWNLOAD,
                          PERMISSION_SIGNATURE_DELETE)

logger = logging.getLogger(__name__)


def document_verify(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VERIFY])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VERIFY, request.user, document)

    document.add_as_recent_document_for_user(request.user)

    try:
        signature = DocumentVersionSignature.objects.verify_signature(document)
    except AttributeError:
        signature_state = SIGNATURE_STATES.get(SIGNATURE_STATE_NONE)
        signature = None
    else:
        signature_state = SIGNATURE_STATES.get(getattr(signature, 'status', None))

    paragraphs = [_(u'Signature status: %s') % signature_state['text']]

    try:
        if DocumentVersionSignature.objects.has_embedded_signature(document):
            signature_type = _(u'Embedded')
        else:
            signature_type = _(u'Detached')
    except ValueError:
        signature_type = _(u'None')

    if signature:
        paragraphs.extend(
            [
                _(u'Signature ID: %s') % signature.signature_id,
                _(u'Signature type: %s') % signature_type,
                _(u'Key ID: %s') % signature.key_id,
                _(u'Timestamp: %s') % datetime.fromtimestamp(int(signature.sig_timestamp)),
                _(u'Signee: %s') % force_escape(getattr(signature, 'username', u'')),
            ]
        )

    return render_to_response('main/generic_template.html', {
        'title': _(u'Signature properties for: %s') % document,
        'object': document,
        'document': document,
        'paragraphs': paragraphs,
    }, context_instance=RequestContext(request))


def document_signature_upload(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SIGNATURE_UPLOAD])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SIGNATURE_UPLOAD, request.user, document)

    document.add_as_recent_document_for_user(request.user)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse('main:home'))))

    if request.method == 'POST':
        form = DetachedSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                DocumentVersionSignature.objects.add_detached_signature(document, request.FILES['file'])
                messages.success(request, _(u'Detached signature uploaded successfully.'))
                return HttpResponseRedirect(next)
            except Exception as exception:
                messages.error(request, exception)
                return HttpResponseRedirect(previous)
    else:
        form = DetachedSignatureForm()

    return render_to_response('main/generic_form.html', {
        'title': _(u'Upload detached signature for: %s') % document,
        'next': next,
        'form': form,
        'previous': previous,
        'object': document,
    }, context_instance=RequestContext(request))


def document_signature_download(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SIGNATURE_DOWNLOAD])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SIGNATURE_DOWNLOAD, request.user, document)

    try:
        if DocumentVersionSignature.objects.has_detached_signature(document):
            signature = DocumentVersionSignature.objects.detached_signature(document)
            return serve_file(
                request,
                signature,
                save_as=u'"%s.sig"' % document.filename,
                content_type=u'application/octet-stream'
            )
    except Exception as exception:
        messages.error(request, exception)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def document_signature_delete(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_SIGNATURE_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_SIGNATURE_DELETE, request.user, document)

    document.add_as_recent_document_for_user(request.user)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse('main:home'))))

    if request.method == 'POST':
        try:
            DocumentVersionSignature.objects.clear_detached_signature(document)
            messages.success(request, _(u'Detached signature deleted successfully.'))
            return HttpResponseRedirect(next)
        except Exception as exception:
            messages.error(request, _(u'Error while deleting the detached signature; %s') % exception)
            return HttpResponseRedirect(previous)

    return render_to_response('main/generic_confirm.html', {
        'title': _(u'Are you sure you wish to delete the detached signature from document: %s?') % document,
        'next': next,
        'previous': previous,
        'object': document,
        'delete_view': True,
    }, context_instance=RequestContext(request))
