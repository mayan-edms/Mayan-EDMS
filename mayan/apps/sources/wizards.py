from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from common.mixins import ViewPermissionCheckMixin
from documents.forms import DocumentTypeSelectForm
from documents.permissions import permission_document_create
from metadata.forms import MetadataFormSet

from .models import InteractiveSource


class DocumentCreateWizard(ViewPermissionCheckMixin, SessionWizardView):
    form_list = (DocumentTypeSelectForm, MetadataFormSet)
    template_name = 'appearance/generic_wizard.html'
    extra_context = {}
    view_permission = permission_document_create

    @staticmethod
    def _has_metadata_types(wizard):
        # Skip the 2nd step if document type has no associated metadata
        try:
            return wizard.get_cleaned_data_for_step('0')['document_type'].metadata.all().count()
        except TypeError:
            return False

    def dispatch(self, request, *args, **kwargs):
        if InteractiveSource.objects.filter(enabled=True).count() == 0:
            messages.error(
                request,
                _(
                    'No interactive document sources have been defined or '
                    'none have been enabled, create one before proceeding.'
                )
            )
            return HttpResponseRedirect(reverse('sources:setup_source_list'))
        return super(
            DocumentCreateWizard, self
        ).dispatch(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(DocumentCreateWizard, self).__init__(*args, **kwargs)

        self.condition_dict = {'1': DocumentCreateWizard._has_metadata_types}

        self.step_titles = [
            _('Step 1 of 2: Select document type'),
            _('Step 2 of 2: Enter document metadata'),
        ]

    def get_form_initial(self, step):
        if step == '1':
            initial = []

            for document_type_metadata_type in self.get_cleaned_data_for_step('0')['document_type'].metadata.all():
                initial.append({
                    'document_type': self.get_cleaned_data_for_step('0')['document_type'],
                    'metadata_type': document_type_metadata_type.metadata_type,
                })

            return initial
        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super(
            DocumentCreateWizard, self
        ).get_context_data(form=form, **kwargs)
        context.update({
            'step_title': self.step_titles[self.steps.step0],
            'submit_label': _('Next step'),
            'submit_icon': 'fa fa-arrow-right',
            'title': _('Document upload wizard'),
        })
        return context

    def done(self, *args, **kwargs):
        query_dict = {}
        try:
            query_dict['document_type_id'] = self.get_cleaned_data_for_step('0')['document_type'].pk
        except AttributeError:
            pass

        try:
            for identifier, metadata in enumerate(self.get_cleaned_data_for_step('1')):
                if metadata.get('update'):
                    query_dict['metadata%s_id' % identifier] = metadata['id']
                    query_dict['metadata%s_value' % identifier] = metadata['value']
        except TypeError:
            pass

        url = '?'.join(
            [
                reverse('sources:upload_interactive'),
                urlencode(query_dict, doseq=True)
            ]
        )
        return HttpResponseRedirect(url)
