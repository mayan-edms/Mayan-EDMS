import logging

from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import (
    ConfirmView, SingleObjectDetailView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from ..events import event_document_view
from ..forms import DocumentVersionDownloadForm, DocumentVersionPreviewForm
from ..models.document_models import Document
from ..models.document_version_models import DocumentVersion
from ..permissions import (
    permission_document_version_revert, permission_document_version_view
)

from .document_views import DocumentDownloadFormView, DocumentDownloadView

__all__ = (
    'DocumentVersionDownloadFormView', 'DocumentVersionDownloadView',
    'DocumentVersionListView', 'DocumentVersionRevertView',
    'DocumentVersionView'
)
logger = logging.getLogger(name=__name__)


class DocumentVersionDownloadFormView(DocumentDownloadFormView):
    form_class = DocumentVersionDownloadForm
    pk_url_kwarg = 'document_version_id'
    querystring_form_fields = (
        'compressed', 'zip_filename', 'preserve_extension'
    )
    source_queryset = DocumentVersion.valid
    viewname = 'documents:document_multiple_version_download'

    def get_extra_context(self):
        result = super(
            DocumentVersionDownloadFormView, self
        ).get_extra_context()

        result.update({
            'title': _('Download document version'),
        })

        return result


class DocumentVersionDownloadView(DocumentDownloadView):
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid

    def get_item_filename(self, item):
        preserve_extension = self.request.GET.get(
            'preserve_extension', self.request.POST.get(
                'preserve_extension', False
            )
        )

        preserve_extension = preserve_extension == 'true' or preserve_extension == 'True'

        return item.get_rendered_string(preserve_extension=preserve_extension)


class DocumentVersionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid

    def get_document(self):
        document = self.external_object
        document.add_as_recent_document_for_user(user=self.request.user)
        return document

    def get_extra_context(self):
        return {
            'hide_object': True,
            'list_as_items': True,
            'object': self.get_document(),
            'table_cell_container_classes': 'td-container-thumbnail',
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


class DocumentVersionRevertView(ExternalObjectMixin, ConfirmView):
    external_object_permission = permission_document_version_revert
    external_object_pk_url_kwarg = 'document_version_id'
    external_object_queryset = DocumentVersion.valid

    def get_extra_context(self):
        return {
            'message': _(
                'All later version after this one will be deleted too.'
            ),
            'object': self.external_object.document,
            'title': _('Revert to this version?'),
        }

    def view_action(self):
        try:
            self.external_object.revert(_user=self.request.user)
            messages.success(
                message=_(
                    'Document version reverted successfully'
                ), request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error reverting document version; %s') % exception,
                request=self.request
            )


class DocumentVersionView(SingleObjectDetailView):
    form_class = DocumentVersionPreviewForm
    object_permission = permission_document_version_view
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid

    def dispatch(self, request, *args, **kwargs):
        result = super(
            DocumentVersionView, self
        ).dispatch(request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            request.user
        )
        event_document_view.commit(
            actor=request.user, target=self.object.document
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of document version: %s') % self.object,
        }
