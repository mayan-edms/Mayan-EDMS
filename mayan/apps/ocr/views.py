from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.documents.forms.document_type_forms import DocumentTypeFilteredSelectForm
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.models.document_version_models import DocumentVersion
from mayan.apps.documents.models.document_version_page_models import DocumentVersionPage

from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import DocumentVersionPageOCRContentForm, DocumentVersionOCRContentForm
from .models import DocumentVersionPageOCRContent, DocumentVersionOCRError
from .permissions import (
    permission_document_version_ocr_content_view, permission_document_version_ocr,
    permission_document_type_ocr_setup
)
from .utils import get_instance_ocr_content


class DocumentVersionOCRContentDeleteView(MultipleObjectConfirmActionView):
    object_permission = permission_document_version_ocr
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid
    success_message = 'Deleted OCR content of %(count)d document version.'
    success_message_plural = 'Deleted OCR content of %(count)d document versions.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Delete the OCR content of the selected document version?',
                plural='Delete the OCR content of the selected document versions?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        DocumentVersionPageOCRContent.objects.delete_content_for(
            document_version=instance, user=self.request.user
        )


class DocumentVersionOCRContentView(SingleObjectDetailView):
    form_class = DocumentVersionOCRContentForm
    object_permission = permission_document_version_ocr_content_view
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(
            request, *args, **kwargs
        )
        self.object.document.add_as_recent_document_for_user(user=request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.object,
            'hide_labels': True,
            'object': self.object,
            'title': _('OCR result for document: %s') % self.object,
        }


class DocumentVersionOCRDownloadView(SingleObjectDownloadView):
    object_permission = permission_document_version_ocr_content_view
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid

    def get_download_file_object(self):
        return get_instance_ocr_content(instance=self.object)

    def get_download_filename(self):
        return '{}-OCR'.format(self.object)


class DocumentVersionOCRErrorsListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_permission = permission_document_version_ocr
    external_object_pk_url_kwarg = 'document_version_id'
    external_object_queryset = DocumentVersion.valid

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'title': _('OCR errors for document: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.ocr_errors.all()


class DocumentVersionOCRSubmitView(MultipleObjectConfirmActionView):
    object_permission = permission_document_version_ocr
    pk_url_kwarg = 'document_version_id'
    source_queryset = DocumentVersion.valid
    success_message = '%(count)d document version submitted to the OCR queue.'
    success_message_plural = '%(count)d document versions submitted to the OCR queue.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Submit the selected document version to the OCR queue?',
                plural='Submit the selected document versions to the OCR queue?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        instance.submit_for_ocr(_user=self.request.user)


class DocumentVersionPageOCRContentView(SingleObjectDetailView):
    form_class = DocumentVersionPageOCRContentForm
    object_permission = permission_document_version_ocr_content_view
    pk_url_kwarg = 'document_version_page_id'
    source_queryset = DocumentVersionPage.valid

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(
            request, *args, **kwargs
        )
        self.object.document_version.document.add_as_recent_document_for_user(
            user=request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('OCR result for document version page: %s') % self.object,
        }


class DocumentTypeSubmitView(FormView):
    extra_context = {
        'title': _('Submit all documents of a type for OCR')
    }
    form_class = DocumentTypeFilteredSelectForm
    post_action_redirect = reverse_lazy(viewname='common:tools_list')

    def form_valid(self, form):
        count = 0

        valid_documents_queryset = Document.valid.all()

        for document_type in form.cleaned_data['document_type']:
            for document in document_type.documents.filter(pk__in=valid_documents_queryset.values('pk')):
                document.submit_for_ocr(_user=self.request.user)
                count += 1

        messages.success(
            message=_(
                '%(count)d documents added to the OCR queue.'
            ) % {
                'count': count,
            }, request=self.request
        )

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_form_extra_kwargs(self):
        return {
            'allow_multiple': True,
            'permission': permission_document_version_ocr,
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')


class DocumentTypeSettingsEditView(ExternalObjectViewMixin, SingleObjectEditView):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_ocr_setup
    external_object_pk_url_kwarg = 'document_type_id'
    fields = ('auto_ocr',)
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )

    def get_document_type(self):
        return self.external_object

    def get_extra_context(self):
        return {
            'object': self.get_document_type(),
            'title': _(
                'Edit OCR settings for document type: %s.'
            ) % self.get_document_type()
        }

    def get_object(self, queryset=None):
        return self.get_document_type().ocr_settings


class EntryListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('OCR errors'),
    }
    view_permission = permission_document_type_ocr_setup

    def get_source_queryset(self):
        return DocumentVersionOCRError.objects.all()
