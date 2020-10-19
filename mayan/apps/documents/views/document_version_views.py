import logging

from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, MultipleObjectDeleteView,
    SingleObjectCreateView, SingleObjectDetailView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from ..events import event_document_viewed
from ..forms.document_version_forms import (
    DocumentVersionForm, DocumentVersionPreviewForm
)
from ..icons import icon_document_version_list
from ..links.document_version_links import link_document_version_create
from ..models.document_models import Document
from ..models.document_version_models import DocumentVersion
from ..permissions import (
    permission_document_version_create, permission_document_version_delete,
    permission_document_version_edit, permission_document_version_export,
    permission_document_version_print, permission_document_version_view
)
from ..tasks import task_document_version_export

from .misc_views import DocumentPrintFormView, DocumentPrintView

__all__ = (
    'DocumentVersionCreateView', 'DocumentVersionListView',
    'DocumentVersionPreviewView'
)
logger = logging.getLogger(name=__name__)


class DocumentVersionCreateView(ExternalObjectMixin, SingleObjectCreateView):
    external_object_class = Document
    external_object_permission = permission_document_version_create
    external_object_pk_url_kwarg = 'document_id'
    form_class = DocumentVersionForm

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                'Create a document version for document: %s'
            ) % self.external_object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'document': self.external_object
        }

    def get_queryset(self):
        return self.external_object.versions.all()


class DocumentVersionDeleteView(MultipleObjectDeleteView):
    model = DocumentVersion
    object_permission = permission_document_version_delete
    pk_url_kwarg = 'document_version_id'

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='documents:document_version_list', kwargs={
                'document_id': self.object_list[0].document_id
            }
        )


class DocumentVersionEditView(SingleObjectEditView):
    form_class = DocumentVersionForm
    model = DocumentVersion
    object_permission = permission_document_version_edit
    pk_url_kwarg = 'document_version_id'

    def get_extra_context(self):
        return {
            'title': _('Edit document version: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_version_preview', kwargs={
                'document_version_id': self.object.pk
            }
        )


class DocumentVersionExportView(MultipleObjectConfirmActionView):
    model = DocumentVersion
    object_permission = permission_document_version_export
    pk_url_kwarg = 'document_version_id'
    success_message = _(
        '%(count)d document version queued for export.'
    )
    success_message_plural = _(
        '%(count)d document versions queued for export.'
    )

    def get_extra_context(self):
        context = {
            'message': _(
                'The process will be performed in the background. '
                'The exported file will be available in the downloads area.'
            ),
            'title': ungettext(
                singular='Export the selected document version?',
                plural='Export the selected document versions?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            context['object'] = self.object_list.first()

        return context

    def object_action(self, form, instance):
        task_document_version_export.apply_async(
            kwargs={'document_version_id': instance.pk}
        )


class DocumentVersionListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_document_version_view
    external_object_pk_url_kwarg = 'document_id'

    def get_document(self):
        document = self.external_object
        document.add_as_recent_document_for_user(user=self.request.user)
        return document

    def get_extra_context(self):
        return {
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_version_list,
            'no_results_main_link': link_document_version_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Versions are views that can display document file pages as '
                'they are, remap or merge them into different layouts.'
            ),
            'no_results_title': _('No versions available'),
            'object': self.get_document(),
            'table_cell_container_classes': 'td-container-thumbnail',
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


class DocumentVersionPreviewView(SingleObjectDetailView):
    form_class = DocumentVersionPreviewForm
    model = DocumentVersion
    object_permission = permission_document_version_view
    pk_url_kwarg = 'document_version_id'

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            user=request.user
        )
        event_document_viewed.commit(
            actor=request.user, action_object=self.object,
            target=self.object.document
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of document version: %s') % self.object,
        }


class DocumentVersionPrintFormView(DocumentPrintFormView):
    external_object_class = DocumentVersion
    external_object_permission = permission_document_version_print
    external_object_pk_url_kwarg = 'document_version_id'
    print_view_name = 'documents:document_version_print_view'
    print_view_kwarg = 'document_version_id'

    def _add_recent_document(self):
        self.external_object.document.add_as_recent_document_for_user(
            user=self.request.user
        )


class DocumentVersionPrintView(DocumentPrintView):
    external_object_class = DocumentVersion
    external_object_permission = permission_document_version_print
    external_object_pk_url_kwarg = 'document_version_id'

    def _add_recent_document(self):
        self.external_object.document.add_as_recent_document_for_user(
            user=self.request.user
        )
