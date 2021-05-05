import logging

from django.conf import settings
from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.sources.links import link_document_file_upload
from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, MultipleObjectDeleteView,
    SingleObjectDetailView, SingleObjectDownloadView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..events import event_document_viewed
from ..forms.document_file_forms import (
    DocumentFileForm, DocumentFilePreviewForm, DocumentFilePropertiesForm
)
from ..forms.misc_forms import PageNumberForm
from ..icons import icon_document_file_list
from ..models.document_models import Document
from ..models.document_file_models import DocumentFile
from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_edit, permission_document_file_print,
    permission_document_file_view
)

from .misc_views import PrintFormView, DocumentPrintView

__all__ = (
    'DocumentFileDeleteView', 'DocumentFileDownloadView',
    'DocumentFileListView', 'DocumentFilePreviewView'
)
logger = logging.getLogger(name=__name__)


class DocumentFileDeleteView(MultipleObjectDeleteView):
    error_message = _(
        'Error deleting document file "%(instance)s"; %(exception)s'
    )
    object_permission = permission_document_file_delete
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid
    success_message_single = _(
        'Document file "%(object)s" deleted successfully.'
    )
    success_message_singular = _(
        '%(count)d document file deleted successfully.'
    )
    success_message_plural = _(
        '%(count)d document files deleted successfully.'
    )
    title_single = _('Delete document file: %(object)s.')
    title_singular = _('Delete the %(count)d selected document file.')
    title_plural = _('Delete the %(count)d selected document files.')

    def get_extra_context(self):
        context = {
            'message': _(
                'All document files pages from this document file and the '
                'document version pages linked to them will be deleted too.'
            )
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_file_list', kwargs={
                'document_id': self.object_list.first().document.pk
            }
        )


class DocumentFileDownloadView(SingleObjectDownloadView):
    object_permission = permission_document_file_download
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

    def get_download_file_object(self):
        instance = self.get_object()
        instance._event_action_object = instance.document
        instance._event_actor = self.request.user
        return instance.get_download_file_object()

    def get_download_filename(self):
        return self.object.filename


class DocumentFileEditView(SingleObjectEditView):
    form_class = DocumentFileForm
    object_permission = permission_document_file_edit
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

    def get_extra_context(self):
        return {
            'title': _('Edit document file: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_file_preview', kwargs={
                'document_file_id': self.object.pk
            }
        )


class DocumentFileListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_document_file_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid

    def get_document(self):
        document = self.external_object
        document.add_as_recent_document_for_user(user=self.request.user)
        return document

    def get_extra_context(self):
        document = self.get_document()
        return {
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_file_list,
            'no_results_main_link': link_document_file_upload.resolve(
                context=RequestContext(
                    dict_={'object': document},
                    request=self.request
                )
            ),
            'no_results_text': _(
                'File are the actual files that were uploaded for each '
                'document. Their contents needs to be mapped to a version '
                'before it can be used.'
            ),
            'no_results_title': _('No files available'),
            'object': document,
            'table_cell_container_classes': 'td-container-thumbnail',
            'title': _('Files of document: %s') % document,
        }

    def get_source_queryset(self):
        return self.get_document().files.order_by('-timestamp')


class DocumentFilePreviewView(SingleObjectDetailView):
    form_class = DocumentFilePreviewForm
    object_permission = permission_document_file_view
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

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
            'title': _('Preview of document file: %s') % self.object,
        }


class DocumentFilePrintFormView(PrintFormView):
    external_object_permission = permission_document_file_print
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid
    print_view_name = 'documents:document_file_print_view'
    print_view_kwarg = 'document_file_id'

    def _add_recent_document(self):
        self.external_object.document.add_as_recent_document_for_user(
            user=self.request.user
        )


class DocumentFilePrintView(DocumentPrintView):
    external_object_permission = permission_document_file_print
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid

    def _add_recent_document(self):
        self.external_object.document.add_as_recent_document_for_user(
            user=self.request.user
        )


class DocumentFilePropertiesView(SingleObjectDetailView):
    form_class = DocumentFilePropertiesForm
    object_permission = permission_document_file_view
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            user=request.user
        )
        return result

    def get_extra_context(self):
        return {
            'document_file': self.object,
            'object': self.object,
            'title': _('Properties of document file: %s') % self.object,
        }


class DocumentFileTransformationsClearView(MultipleObjectConfirmActionView):
    object_permission = permission_transformation_delete
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid
    success_message = _(
        'Transformation clear request processed for %(count)d document file.'
    )
    success_message_plural = _(
        'Transformation clear request processed for %(count)d document files.'
    )

    def get_extra_context(self):
        result = {
            'title': ungettext(
                singular='Clear all the page transformations for the selected document file?',
                plural='Clear all the page transformations for the selected document files?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _(
                        'Clear all the page transformations for the '
                        'document file: %s?'
                    ) % self.object_list.first()
                }
            )

        return result

    def object_action(self, form, instance):
        try:
            for page in instance.pages.all():
                layer_saved_transformations.get_transformations_for(
                    obj=page
                ).delete()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error deleting the page transformations for '
                    'document file: %(document_file)s; %(error)s.'
                ) % {
                    'document_file': instance, 'error': exception
                }, request=self.request
            )


class DocumentFileTransformationsCloneView(ExternalObjectViewMixin, FormView):
    external_object_permission = permission_transformation_edit
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid
    form_class = PageNumberForm

    def dispatch(self, request, *args, **kwargs):
        results = super().dispatch(request=request, *args, **kwargs)
        self.external_object.document.add_as_recent_document_for_user(
            user=request.user
        )

        return results

    def form_valid(self, form):
        try:
            layer_saved_transformations.copy_transformations(
                delete_existing=True, source=form.cleaned_data['page'],
                targets=form.cleaned_data['page'].siblings.exclude(
                    pk=form.cleaned_data['page'].pk
                )
            )
        except Exception as exception:
            if settings.DEBUG:
                raise
            else:
                messages.error(
                    message=_(
                        'Error cloning the page transformations for '
                        'document file: %(document_file)s; %(error)s.'
                    ) % {
                        'document_file': self.external_object,
                        'error': exception
                    }, request=self.request
                )
        else:
            messages.success(
                message=_('Transformations cloned successfully.'),
                request=self.request
            )

        return super().form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'instance': self.external_object
        }

    def get_extra_context(self):
        context = {
            'object': self.external_object,
            'submit_label': _('Submit'),
            'title': _(
                'Clone page transformations of document file: %s'
            ) % self.external_object,
        }

        return context
