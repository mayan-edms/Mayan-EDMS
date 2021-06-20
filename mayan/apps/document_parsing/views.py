from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.documents.forms.document_type_forms import (
    DocumentTypeFilteredSelectForm
)
from mayan.apps.documents.models.document_file_models import DocumentFile
from mayan.apps.documents.models.document_file_page_models import DocumentFilePage
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import DocumentFileContentForm, DocumentFilePageContentForm
from .models import DocumentFileParseError, DocumentFilePageContent
from .permissions import (
    permission_document_file_content_view, permission_document_type_parsing_setup,
    permission_document_file_parse
)
from .utils import get_document_file_content


class DocumentFileContentDeleteView(MultipleObjectConfirmActionView):
    object_permission = permission_document_file_parse
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid
    success_message = 'Deleted parsed content of %(count)d document file.'
    success_message_plural = 'Deleted parsed content of %(count)d document files.'

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Delete the parsed content of the selected document file?',
                plural='Delete the parsed content of the selected document files?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result['object'] = queryset.first()

        return result

    def object_action(self, form, instance):
        DocumentFilePageContent.objects.delete_content_for(
            document_file=instance, user=self.request.user
        )


class DocumentFileContentDownloadView(SingleObjectDownloadView):
    object_permission = permission_document_file_content_view
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

    def get_download_file_object(self):
        return get_document_file_content(document_file=self.object)

    def get_download_filename(self):
        return '{}-content'.format(self.object)


class DocumentFileContentView(SingleObjectDetailView):
    form_class = DocumentFileContentForm
    object_permission = permission_document_file_content_view
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request=request, *args, **kwargs)
        self.object.document.add_as_recent_document_for_user(
            user=request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Content for document file: %s') % self.object,
        }


class DocumentFilePageContentView(SingleObjectDetailView):
    form_class = DocumentFilePageContentForm
    object_permission = permission_document_file_content_view
    pk_url_kwarg = 'document_file_page_id'
    source_queryset = DocumentFilePage.valid

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request=request, *args, **kwargs)
        self.object.document_file.document.add_as_recent_document_for_user(
            request.user
        )
        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Content for document file page: %s') % self.object,
        }

    def get_source_queryset(self):
        document_file_queryset = DocumentFile.valid.all()
        return DocumentFilePage.objects.filter(
            document_file_id__in=document_file_queryset.values('pk')
        )


class DocumentFileParsingErrorsListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_permission = permission_document_file_parse
    external_object_pk_url_kwarg = 'document_file_id'
    external_object_queryset = DocumentFile.valid

    def get_extra_context(self):
        return {
            'hide_object': True,
            'object': self.external_object,
            'title': _(
                'Parsing errors for document file: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.parsing_errors.all()


class DocumentFileSubmitView(MultipleObjectConfirmActionView):
    object_permission = permission_document_file_parse
    pk_url_kwarg = 'document_file_id'
    source_queryset = DocumentFile.valid
    success_message = _(
        '%(count)d document file added to the parsing queue'
    )
    success_message_plural = _(
        '%(count)d documents files added to the parsing queue'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Submit %(count)d document file to the parsing queue?',
                plural='Submit %(count)d documents files to the parsing queue?',
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
                        'Submit document file "%s" to the parsing queue'
                    ) % queryset.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        instance.submit_for_parsing(_user=self.request.user)


class DocumentTypeSettingsEditView(ExternalObjectViewMixin, SingleObjectEditView):
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
            'permission': permission_document_file_parse,
            'user': self.request.user
        }

    def form_valid(self, form):
        count = 0
        for document_type in form.cleaned_data['document_type']:
            for document in document_type.documents.all():
                document.submit_for_parsing(_user=self.request.user)
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
    view_permission = permission_document_file_parse

    def get_source_queryset(self):
        return DocumentFileParseError.objects.all()
