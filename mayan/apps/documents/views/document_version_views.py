from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import ConfirmView, SingleObjectListView

from ..models import Document, DocumentVersion
from ..permissions import (
    permission_document_download, permission_document_version_revert,
    permission_document_view
)

from .document_views import DocumentDownloadFormView, DocumentDownloadView

logger = logging.getLogger(__name__)


class DocumentVersionListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=request.user,
            obj=self.get_document()
        )

        self.get_document().add_as_recent_document_for_user(request.user)

        return super(
            DocumentVersionListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_object': True, 'object': self.get_document(),
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


class DocumentVersionRevertView(ConfirmView):
    object_permission = permission_document_version_revert
    object_permission_related = 'document'

    def get_extra_context(self):
        return {
            'message': _(
                'All later version after this one will be deleted too.'
            ),
            'object': self.get_object().document,
            'title': _('Revert to this version?'),
        }

    def get_object(self):
        return get_object_or_404(DocumentVersion, pk=self.kwargs['pk'])

    def view_action(self):
        try:
            self.get_object().revert(_user=self.request.user)
            messages.success(
                self.request, _('Document version reverted successfully')
            )
        except Exception as exception:
            messages.error(
                self.request,
                _('Error reverting document version; %s') % exception
            )


class DocumentVersionDownloadFormView(DocumentDownloadFormView):
    model = DocumentVersion
    multiple_download_view = None
    single_download_view = 'documents:document_version_download'

    def get_document_queryset(self):
        id_list = self.request.GET.get(
            'id_list', self.request.POST.get('id_list', '')
        )

        if not id_list:
            id_list = self.kwargs['pk']

        return self.model.objects.filter(
            pk__in=id_list.split(',')
        )


class DocumentVersionDownloadView(DocumentDownloadView):
    model = DocumentVersion
    object_permission = permission_document_download
