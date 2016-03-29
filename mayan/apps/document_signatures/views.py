from __future__ import absolute_import, unicode_literals

import logging

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectListView
)
from documents.models import DocumentVersion
from permissions import Permission

from .forms import DocumentVersionSignatureDetailForm
from .models import DetachedSignature, SignatureBaseModel
from .permissions import (
    permission_document_version_signature_view,
    permission_document_version_signature_upload,
    permission_document_version_signature_download,
    permission_document_version_signature_delete
)

logger = logging.getLogger(__name__)


class DocumentVersionSignatureDeleteView(SingleObjectDeleteView):
    model = DetachedSignature
    object_permission = permission_document_version_signature_delete
    object_permission_related = 'document_version.document'

    def get_extra_context(self):
        return {
            'document': self.get_object().document_version.document,
            'document_version': self.get_object().document_version,
            'navigation_object_list': (
                'document', 'document_version', 'signature'
            ),
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
    object_permission = permission_document_version_signature_view
    object_permission_related = 'document_version.document'

    def get_extra_context(self):
        return {
            'document': self.get_object().document_version.document,
            'document_version': self.get_object().document_version,
            'signature': self.get_object(),
            'navigation_object_list': (
                'document', 'document_version', 'signature'
            ),
            'hide_object': True,
            'title': _(
                'Details for signature: %s'
            ) % self.get_object(),
        }

    def get_queryset(self):
        return SignatureBaseModel.objects.select_subclasses()


class DocumentSignatureDownloadView(SingleObjectDownloadView):
    model = DetachedSignature
    object_permission = permission_document_version_signature_download
    object_permission_related = 'document_version.document'

    def get_file(self):
        signature = self.get_object()

        return DocumentSignatureDownloadView.VirtualFile(
            signature.signature_file, name=unicode(signature)
        )


class DocumentVersionSignatureListView(SingleObjectListView):
    object_permission = permission_document_version_signature_view
    object_permission_related = 'document_version.document'

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
                self.request.user, (
                    permission_document_version_signature_view,
                )
            )
        except PermissionDenied:
            return AccessControlList.objects.filter_by_access(
                permission_document_version_signature_view, self.request.user,
                queryset
            )
        else:
            return queryset


class DocumentVersionSignatureUploadView(SingleObjectCreateView):
    fields = ('signature_file',)
    model = DetachedSignature

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_document_version_signature_upload,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_version_signature_upload, request.user,
                self.get_document_version()
            )

        return super(
            DocumentVersionSignatureUploadView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_version(self):
        return get_object_or_404(DocumentVersion, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'document': self.get_document_version().document,
            'document_version': self.get_document_version(),
            'navigation_object_list': ('document', 'document_version'),
            'title': _(
                'Upload detached signature for document version: %s'
            ) % self.get_document_version(),
        }

    def get_instance_extra_data(self):
        return {'document_version': self.get_document_version()}

    def get_post_action_redirect(self):
        return reverse(
            'signatures:document_version_signature_list',
            args=(self.get_document_version().pk,)
        )
