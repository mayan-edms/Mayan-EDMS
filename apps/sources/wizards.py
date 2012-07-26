from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlencode

from common.wizard import BoundFormWizard
from metadata.forms import MetadataSelectionForm, MetadataFormSet
from documents.forms import DocumentTypeSelectForm


class DocumentCreateWizard(BoundFormWizard):
    def generate_metadata_initial_values(self):
        initial = []
        for metadata_type in self.metadata_types:
            initial.append({
                'metadata_type': metadata_type,
            })

        for metadata_set in self.metadata_sets:
            for metadata_set_item in metadata_set.metadatasetitem_set.all():
                data = {
                    'metadata_type': metadata_set_item.metadata_type,
                }
                if data not in initial:
                    initial.append(data)

        return initial

    def __init__(self, *args, **kwargs):
        self.query_dict = {}
        self.step_titles = kwargs.pop('step_titles', [
            _(u'step 1 of 3: Document type'),
            _(u'step 2 of 3: Metadata selection'),
            _(u'step 3 of 3: Document metadata'),
            ])

        super(DocumentCreateWizard, self).__init__(*args, **kwargs)

    def render_template(self, request, form, previous_fields, step, context=None):
        context = {
            'step_title': self.extra_context['step_titles'][step],
            'submit_label': _(u'Next step'),
            'submit_icon_famfam': 'arrow_right',
        }
        return super(DocumentCreateWizard, self).render_template(
            request, form, previous_fields, step, context
        )

    def parse_params(self, request, *args, **kwargs):
        self.extra_context = {'step_titles': self.step_titles}

    def process_step(self, request, form, step):
        if isinstance(form, DocumentTypeSelectForm):
            self.document_type = form.cleaned_data['document_type']
            self.initial = {1: {'document_type': self.document_type}}

        if isinstance(form, MetadataSelectionForm):
            self.metadata_sets = form.cleaned_data['metadata_sets']
            self.metadata_types = form.cleaned_data['metadata_types']
            initial_data = self.generate_metadata_initial_values()
            self.initial = {2: initial_data}
            if not initial_data:
                # If there is no metadata selected, finish wizard
                self.form_list = [DocumentTypeSelectForm, MetadataSelectionForm]

        if isinstance(form, MetadataFormSet):
            for identifier, metadata in enumerate(form.cleaned_data):
                self.query_dict['metadata%s_id' % identifier] = metadata['id']
                self.query_dict['metadata%s_value' % identifier] = metadata['value']

    def get_template(self, step):
        return 'generic_wizard.html'

    def done(self, request, form_list):
        if self.document_type:
            self.query_dict['document_type_id'] = self.document_type.pk

        url = '?'.join([reverse('upload_interactive'), urlencode(self.query_dict, doseq=True)])
        return HttpResponseRedirect(url)
