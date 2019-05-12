from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.common.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.forms import DocumentTypeFilteredSelectForm
from mayan.apps.documents.models import Document, DocumentPage, DocumentType

from .forms import DocumentContentForm, DocumentPageContentForm
from .models import DocumentVersionParseError
from .permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)
from .utils import get_document_content


class DocumentContentView(SingleObjectDetailView):
    form_class = DocumentContentForm
    model = Document
    object_permission = permission_content_view

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.get_object().add_as_recent_document_for_user(request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.get_object(),
            'hide_labels': True,
            'object': self.get_object(),
            'title': _('Content for document: %s') % self.get_object(),
        }


class DocumentContentDownloadView(SingleObjectDownloadView):
    model = Document
    object_permission = permission_content_view

    def get_file(self):
        file_object = DocumentContentDownloadView.TextIteratorIO(
            iterator=get_document_content(document=self.get_object())
        )
        return DocumentContentDownloadView.VirtualFile(
            file=file_object, name='{}-content'.format(self.get_object())
        )


class DocumentPageContentView(SingleObjectDetailView):
    form_class = DocumentPageContentForm
    model = DocumentPage
    object_permission = permission_content_view

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentPageContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.get_object().document.add_as_recent_document_for_user(
            request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.get_object(),
            'title': _('Content for document page: %s') % self.get_object(),
        }


class DocumentParsingErrorsListView(SingleObjectListView):
    view_permission = permission_content_view

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.get_document(),
            'title': _(
                'Parsing errors for document: %s'
            ) % self.get_document(),
        }

    def get_source_queryset(self):
        return self.get_document().latest_version.parsing_errors.all()


class DocumentSubmitView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_parse_document
    success_message = _(
        '%(count)d document added to the parsing queue'
    )
    success_message_plural = _(
        '%(count)d documents added to the parsing queue'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Submit %(count)d document to the parsing queue?',
                plural='Submit %(count)d documents to the parsing queue',
                number=queryset.count()
            ) % {
                'count': queryset.count(),
            }
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Submit document "%s" to the parsing queue'
                    ) % queryset.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        instance.submit_for_parsing()


class DocumentTypeSettingsEditView(ExternalObjectMixin, SingleObjectEditView):
    external_object_class = DocumentType
    external_object_permission = permission_document_type_parsing_setup
    external_object_pk_url_kwarg = 'pk'
    fields = ('auto_parsing',)
    post_action_redirect = reverse_lazy(viewname='documents:document_type_list')

    def get_document_type(self):
        return self.external_object

    def get_extra_context(self):
        return {
            'object': self.get_document_type(),
            'title': _(
                'Edit parsing settings for document type: %s.'
            ) % self.get_document_type()
        }

    def get_object(self, queryset=None):
        return self.get_document_type().parsing_settings


class DocumentTypeSubmitView(FormView):
    extra_context = {
        'title': _('Submit all documents of a type for parsing.')
    }
    form_class = DocumentTypeFilteredSelectForm
    post_action_redirect = reverse_lazy(viewname='common:tools_list')

    def get_form_extra_kwargs(self):
        return {
            'allow_multiple': True,
            'permission': permission_parse_document,
            'user': self.request.user
        }

    def form_valid(self, form):
        count = 0
        for document_type in form.cleaned_data['document_type']:
            for document in document_type.documents.all():
                document.submit_for_parsing()
                count += 1

        messages.success(
            message=_(
                '%(count)d documents added to the parsing queue.'
            ) % {
                'count': count,
            }, requrest=self.request
        )

        return HttpResponseRedirect(redirect_to=self.get_success_url())


class ParseErrorListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Parsing errors'),
    }
    view_permission = permission_document_type_parsing_setup

    def get_source_queryset(self):
        return DocumentVersionParseError.objects.all()
