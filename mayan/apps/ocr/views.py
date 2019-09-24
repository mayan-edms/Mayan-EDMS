from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.common.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.forms import DocumentTypeFilteredSelectForm
from mayan.apps.documents.models import Document, DocumentPage, DocumentType

from .forms import DocumentPageOCRContentForm, DocumentOCRContentForm
from .models import DocumentPageOCRContent, DocumentVersionOCRError
from .permissions import (
    permission_ocr_content_view, permission_ocr_document,
    permission_document_type_ocr_setup
)
from .utils import get_document_ocr_content


class DocumentOCRContentDeleteView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_ocr_document
    success_message = 'Deleted OCR content of %(count)d document.'
    success_message_plural = 'Deleted OCR content of %(count)d documents.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Delete the OCR content of the selected document?',
                plural='Delete the OCR content of the selected documents?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        DocumentPageOCRContent.objects.delete_content_for(
            document=instance, user=self.request.user
        )


class DocumentOCRContentView(SingleObjectDetailView):
    form_class = DocumentOCRContentForm
    model = Document
    object_permission = permission_ocr_content_view

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentOCRContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.get_object().add_as_recent_document_for_user(user=request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.get_object(),
            'hide_labels': True,
            'object': self.get_object(),
            'title': _('OCR result for document: %s') % self.get_object(),
        }


class DocumentPageOCRContentView(SingleObjectDetailView):
    form_class = DocumentPageOCRContentForm
    model = DocumentPage
    object_permission = permission_ocr_content_view

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentPageOCRContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.get_object().document.add_as_recent_document_for_user(
            user=request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.get_object(),
            'title': _('OCR result for document page: %s') % self.get_object(),
        }


class DocumentSubmitView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_ocr_document
    success_message = '%(count)d document submitted to the OCR queue.'
    success_message_plural = '%(count)d documents submitted to the OCR queue.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Submit the selected document to the OCR queue?',
                plural='Submit the selected documents to the OCR queue?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        instance.submit_for_ocr()


class DocumentTypeSubmitView(FormView):
    extra_context = {
        'title': _('Submit all documents of a type for OCR')
    }
    form_class = DocumentTypeFilteredSelectForm
    post_action_redirect = reverse_lazy(viewname='common:tools_list')

    def form_valid(self, form):
        count = 0
        for document_type in form.cleaned_data['document_type']:
            for document in document_type.documents.all():
                document.submit_for_ocr()
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
            'permission': permission_ocr_document,
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')


class DocumentTypeSettingsEditView(ExternalObjectMixin, SingleObjectEditView):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_ocr_setup
    external_object_pk_url_kwarg = 'pk'
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


class DocumentOCRErrorsListView(SingleObjectListView):
    object_permission = permission_ocr_document

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.get_document(),
            'title': _('OCR errors for document: %s') % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().latest_version.ocr_errors.all()


class DocumentOCRDownloadView(SingleObjectDownloadView):
    model = Document
    object_permission = permission_ocr_content_view

    def get_file(self):
        file_object = DocumentOCRDownloadView.TextIteratorIO(
            iterator=get_document_ocr_content(document=self.get_object())
        )
        return DocumentOCRDownloadView.VirtualFile(
            file=file_object, name='{}-OCR'.format(self.get_object())
        )
