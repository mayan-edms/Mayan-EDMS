from __future__ import absolute_import

from datetime import datetime
import logging

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template.defaultfilters import force_escape
from django.core.exceptions import PermissionDenied

from documents.models import Document, RecentDocument
from permissions.models import Permission
from filetransfers.api import serve_file
from acls.models import AccessEntry

from django_gpg.api import SIGNATURE_STATES

from . import (PERMISSION_DOCUMENT_VERIFY, PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD)
from .forms import DetachedSignatureForm
from .models import DocumentVersionSignature

logger = logging.getLogger(__name__)


def document_verify(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VERIFY])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VERIFY, request.user, document)

    RecentDocument.objects.add_document_for_user(request.user, document)

    signature = DocumentVersionSignature.objects.verify_signature(document)

    signature_state = SIGNATURE_STATES.get(getattr(signature, 'status', None))

    widget = (u'<img style="vertical-align: middle;" src="%simages/icons/%s" />' % (settings.STATIC_URL, signature_state['icon']))
    paragraphs = [
        _(u'Signature status: %(widget)s %(text)s') % {
            'widget': mark_safe(widget),
            'text': signature_state['text']
        },
    ]

    if DocumentVersionSignature.objects.has_embedded_signature(document):
        signature_type = _(u'embedded')
    else:
        signature_type = _(u'detached')

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

    return render_to_response('generic_template.html', {
        'title': _(u'signature properties for: %s') % document,
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

    RecentDocument.objects.add_document_for_user(request.user, document)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = DetachedSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                DocumentVersionSignature.objects.add_detached_signature(document, request.FILES['file'])
                messages.success(request, _(u'Detached signature uploaded successfully.'))
                return HttpResponseRedirect(next)
            except Exception, msg:
                messages.error(request, msg)
                return HttpResponseRedirect(previous)
    else:
        form = DetachedSignatureForm()

    return render_to_response('generic_form.html', {
        'title': _(u'Upload detached signature for: %s') % document,
        'form_icon': 'key_delete.png',
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
    except Exception, e:
        messages.error(request, e)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
