from django.contrib import messages
from django.http import HttpResponseRedirect
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
from .models import DocumentPageContent, DocumentVersionParseError
from .permissions import (
    permission_content_view, permission_document_type_parsing_setup,
    permission_parse_document
)
from .utils import get_instance_content


class DocumentContentDeleteView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_parse_document
    pk_url_kwarg = 'document_id'
    success_message = 'Deleted parsed content of %(count)d document.'
    success_message_plural = 'Deleted parsed content of %(count)d documents.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Delete the parsed content of the selected document?',
                plural='Delete the parsed content of the selected documents?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        DocumentPageContent.objects.delete_content_for(
            document=instance, user=self.request.user
        )


class DocumentContentView(SingleObjectDetailView):
    form_class = DocumentContentForm
    model = Document
    object_permission = permission_content_view
    pk_url_kwarg = 'document_id'

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.object.add_as_recent_document_for_user(request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.object,
            'hide_labels': True,
            'object': self.object,
            'title': _('Content for document: %s') % self.object,
        }


class DocumentContentDownloadView(SingleObjectDownloadView):
    model = Document
    object_permission = permission_content_view
    pk_url_kwarg = 'document_id'

    def get_download_file_object(self):
        return get_instance_content(document=self.object)

    def get_download_filename(self):
        return '{}-content'.format(self.object)


class DocumentPageContentView(SingleObjectDetailView):
    form_class = DocumentPageContentForm
    model = DocumentPage
    object_permission = permission_content_view
    pk_url_kwarg = 'document_page_id'

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentPageContentView, self).dispatch(
            request, *args, **kwargs
        )
        self.object.document.add_as_recent_document_for_user(
            request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Content for document page: %s') % self.object,
        }


class DocumentParsingErrorsListView(
    ExternalObjectMixin, SingleObjectListView
):
    external_object_class = Document
    external_object_permission = permission_parse_document
    external_object_pk_url_kwarg = 'document_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'title': _(
                'Parsing errors for document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.latest_version.parsing_errors.all()


class DocumentSubmitView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_parse_document
    pk_url_kwarg = 'document_id'
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
                plural='Submit %(count)d documents to the parsing queue?',
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
    external_object_pk_url_kwarg = 'document_type_id'
    fields = ('auto_parsing',)
    post_action_redirect = reverse_lazy(
        viewname='documents:document_type_list'
    )

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
        'title': _('Submit all documents of a type for parsing')
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
            }, request=self.request
        )

        return HttpResponseRedirect(redirect_to=self.get_success_url())


class ParseErrorListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Parsing errors'),
    }
    view_permission = permission_parse_document

    def get_source_queryset(self):
        return DocumentVersionParseError.objects.all()
