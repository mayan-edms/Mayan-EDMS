from __future__ import absolute_import, unicode_literals

from datetime import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.defaultfilters import force_escape
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from django_gpg.literals import SIGNATURE_STATE_NONE, SIGNATURE_STATES
from documents.models import Document
from filetransfers.api import serve_file
from permissions import Permission

from .forms import DetachedSignatureForm
from .models import DocumentVersionSignature
from .permissions import (
    permission_document_verify, permission_signature_upload,
    permission_signature_download, permission_signature_delete
)

logger = logging.getLogger(__name__)


def document_verify(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_document_verify,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_verify, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    try:
        signature = DocumentVersionSignature.objects.verify_signature(
            document.latest_version
        )
    except AttributeError:
        signature_state = SIGNATURE_STATES.get(SIGNATURE_STATE_NONE)
        signature = None
    else:
        signature_state = SIGNATURE_STATES.get(
            getattr(signature, 'status', None)
        )

    paragraphs = [_('Signature status: %s') % signature_state['text']]

    try:
        if DocumentVersionSignature.objects.has_embedded_signature(document.latest_version):
            signature_type = _('Embedded')
        else:
            signature_type = _('Detached')
    except ValueError:
        signature_type = _('None')

    if signature:
        paragraphs.extend(
            [
                _('Signature ID: %s') % signature.signature_id,
                _('Signature type: %s') % signature_type,
                _('Key ID: %s') % signature.key_id,
                _('Timestamp: %s') % datetime.fromtimestamp(
                    int(signature.sig_timestamp)
                ),
                _('Signee: %s') % force_escape(getattr(signature, 'username', '')),
            ]
        )

    return render_to_response('appearance/generic_template.html', {
        'document': document,
        'object': document,
        'paragraphs': paragraphs,
        'title': _('Signature properties for document: %s') % document,
    }, context_instance=RequestContext(request))


def document_signature_upload(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_signature_upload,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_signature_upload, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = DetachedSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                DocumentVersionSignature.objects.add_detached_signature(
                    document.latest_version, request.FILES['file']
                )
                messages.success(
                    request, _('Detached signature uploaded successfully.')
                )
                return HttpResponseRedirect(next)
            except Exception as exception:
                messages.error(request, exception)
                return HttpResponseRedirect(previous)
    else:
        form = DetachedSignatureForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'next': next,
        'object': document,
        'previous': previous,
        'title': _('Upload detached signature for document: %s') % document,
    }, context_instance=RequestContext(request))


def document_signature_download(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_signature_download,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_signature_download, request.user, document
        )

    try:
        if DocumentVersionSignature.objects.has_detached_signature(document.latest_version):
            signature = DocumentVersionSignature.objects.detached_signature(
                document.latest_version
            )
            return serve_file(
                request,
                signature,
                save_as='"%s.sig"' % document.filename,
                content_type='application/octet-stream'
            )
    except Exception as exception:
        messages.error(request, exception)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def document_signature_delete(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_signature_delete,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_signature_delete, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            DocumentVersionSignature.objects.clear_detached_signature(
                document.latest_version
            )
            messages.success(
                request, _('Detached signature deleted successfully.')
            )
            return HttpResponseRedirect(next)
        except Exception as exception:
            messages.error(
                request, _(
                    'Error while deleting the detached signature; %s'
                ) % exception
            )
            return HttpResponseRedirect(previous)

    return render_to_response('appearance/generic_confirm.html', {
        'delete_view': True,
        'next': next,
        'object': document,
        'previous': previous,
        'title': _(
            'Delete the detached signature from document: %s?'
        ) % document,
    }, context_instance=RequestContext(request))
