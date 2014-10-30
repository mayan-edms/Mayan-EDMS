from __future__ import absolute_import

from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from common.views import MayanPermissionCheckMixin
from documents.forms import DocumentTypeSelectForm
from documents.permissions import PERMISSION_DOCUMENT_CREATE
from metadata.forms import MetadataFormSet


class DocumentCreateWizard(MayanPermissionCheckMixin, SessionWizardView):
    form_list = [DocumentTypeSelectForm, MetadataFormSet]
    template_name = 'main/generic_wizard.html'
    extra_context = {}
    permissions_required = [PERMISSION_DOCUMENT_CREATE]

    @staticmethod
    def _has_metadata_types(wizard):
        # Skip the 2nd step if document type has no associated metadata
        try:
            return wizard.get_cleaned_data_for_step('0')['document_type'].metadata_type.all().count()
        except TypeError:
            return False

    def __init__(self, *args, **kwargs):
        super(DocumentCreateWizard, self).__init__(*args, **kwargs)

        self.condition_dict = {'1': DocumentCreateWizard._has_metadata_types}

        self.step_titles = [
            _(u'Step 1 of 2: Select document type'),
            _(u'Step 2 of 2: Enter document metadata'),
        ]

    def get_form_initial(self, step):
        if step == '1':
            initial = []

            for metadata_type in self.get_cleaned_data_for_step('0')['document_type'].metadata_type.filter(required=True):
                initial.append({
                    'metadata_type': metadata_type,
                    'required': True,
                })

            for metadata_type in self.get_cleaned_data_for_step('0')['document_type'].metadata_type.filter(required=False):
                initial.append({
                    'metadata_type': metadata_type,
                })


            return initial
        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super(DocumentCreateWizard, self).get_context_data(form=form, **kwargs)
        context.update({
            'step_title': self.step_titles[self.steps.step0],
            'submit_label': _(u'Next step'),
            'submit_icon_famfam': 'arrow_right',
        })
        return context

    def done(self, form_list):
        query_dict = {}
        try:
            query_dict['document_type_id'] = self.get_cleaned_data_for_step('0')['document_type'].pk
        except AttributeError:
            pass

        try:
            for identifier, metadata in enumerate(self.get_cleaned_data_for_step('1')):
                query_dict['metadata%s_id' % identifier] = metadata['id']
                query_dict['metadata%s_value' % identifier] = metadata['value']
        except TypeError:
            pass

        url = '?'.join([reverse('sources:upload_interactive'), urlencode(query_dict, doseq=True)])
        return HttpResponseRedirect(url)
