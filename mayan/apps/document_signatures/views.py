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
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import (
    SingleObjectDeleteView, SingleObjectDetailView, SingleObjectListView
)
from django_gpg.literals import SIGNATURE_STATE_NONE, SIGNATURE_STATES
from documents.models import Document, DocumentVersion
from filetransfers.api import serve_file
from permissions import Permission

from .forms import DetachedSignatureForm, DocumentVersionSignatureDetailForm
from .models import DetachedSignature, SignatureBaseModel
from .permissions import (
    permission_document_version_signature_view,
    permission_document_version_signature_verify,
    permission_document_version_signature_upload,
    permission_document_version_signature_download,
    permission_document_version_signature_delete
)

logger = logging.getLogger(__name__)


class DocumentVersionSignatureDeleteView(SingleObjectDeleteView):
    model = DetachedSignature

    def get_extra_context(self):
        return {
            'document': self.get_object().document_version.document,
            'document_version': self.get_object().document_version,
            'navigation_object_list': ('document', 'document_version', 'signature'),
            'signature': self.get_object(),
            'title': _('Delete detached signature: %s') % self.get_object()
        }

    def get_post_action_redirect(self):
        return reverse(
            'signatures:document_version_signature_list',
            args=(self.get_object().document_version.pk,)
        )


class DocumentVersionSignatureDetailView(SingleObjectDetailView):
    form_class = DocumentVersionSignatureDetailForm

    def get_extra_context(self):
        return {
            'document': self.get_object().document_version.document,
            'document_version': self.get_object().document_version,
            'signature': self.get_object(),
            'navigation_object_list': ('document', 'document_version', 'signature'),
            'hide_object': True,
            'title': _(
                'Details for signature: %s'
            ) % self.get_object(),
        }

    def get_queryset(self):
        return SignatureBaseModel.objects.select_subclasses()


class DocumentVersionSignatureListView(SingleObjectListView):
    def get_document_version(self):
        return get_object_or_404(DocumentVersion, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'document': self.get_document_version().document,
            'document_version': self.get_document_version(),
            'navigation_object_list': ('document', 'document_version'),
            'hide_object': True,
            'title': _(
                'Signatures for document version: %s'
            ) % self.get_document_version(),
        }

    def get_queryset(self):
        queryset = self.get_document_version().signatures.all()

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_version_signature_view,)
            )
        except PermissionDenied:
            return AccessControlList.objects.filter_by_access(
                permission_document_version_signature_view, self.request.user, queryset
            )
        else:
            return queryset


def document_version_signature_upload(request, pk):
    document_version = get_object_or_404(DocumentVersion, pk=pk)

    try:
        Permission.check_permissions(
            request.user, (permission_document_version_signature_upload,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_version_signature_upload, request.user, document_version.document
        )

    document_version.document.add_as_recent_document_for_user(request.user)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = DetachedSignatureForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                DetachedSignature.objects.create(
                    document_version=document_version,
                    signature_file=request.FILES['file']
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
        'document': document_version.document,
        'document_version': document_version,
        'navigation_object_list': ('document', 'document_version'),
        'previous': previous,
        'title': _('Upload detached signature for document version: %s') % document_version,
    }, context_instance=RequestContext(request))


def document_signature_download(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)

    try:
        Permission.check_permissions(
            request.user, (permission_document_version_signature_download,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_version_signature_download, request.user, document
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
