from django import forms
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.core.urlresolvers import reverse

from common.wizard import BoundFormWizard
from common.utils import urlquote
from common.forms import DetailForm

from models import Document, DocumentType, DocumentTypeMetadataType


from documents.conf.settings import AVAILABLE_FUNCTIONS


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'document_type' in kwargs['initial']:
                self.fields['document_type'].widget = forms.HiddenInput()

    class Meta:
        model = Document


class DocumentForm_view(DetailForm):
    class Meta:
        model = Document
        exclude = ('file',)

class DocumentTypeSelectForm(forms.Form):
    document_type = forms.ModelChoiceField(queryset=DocumentType.objects.all())


class MetadataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs)
        
        #Set form fields initial values
        if 'initial' in kwargs:
            self.metadata_type = kwargs['initial'].pop('metadata_type', None)
            self.document_type = kwargs['initial'].pop('document_type', None)
            self.metadata_options = kwargs['initial'].pop('metadata_options', None)
      
            self.fields['name'].initial=self.metadata_type.name
            self.fields['id'].initial=self.metadata_type.id
            if self.metadata_type.default:
                try:
                    self.fields['value'].initial = eval(self.metadata_type.default, AVAILABLE_FUNCTIONS)
                except Exception, err:
                    self.fields['value'].initial = err

    id = forms.CharField(label=_(u'id'), widget=forms.HiddenInput)
    name = forms.CharField(label=_(u'Name'),
        required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    value = forms.CharField(label=_(u'Value'))


class DocumentCreateWizard(BoundFormWizard):
    def render_template(self, request, form, previous_fields, step, context=None):
        context = {'step_title':self.extra_context['step_titles'][step]}
        return super(DocumentCreateWizard, self).render_template(request, form, previous_fields, step, context)

    def parse_params(self, request, *args, **kwargs):
        self.extra_context={'step_titles':[
            _(u'step 1 of 2: Document type'),
            _(u'step 2 of 2: Document metadata'),
            ]}
            
    def process_step(self, request, form, step):
        if step == 0:
            self.document_type = form.cleaned_data['document_type']

            initial=[]
            for item in DocumentTypeMetadataType.objects.filter(document_type=self.document_type):
                initial.append({
                    'metadata_type':item.metadata_type,
                    'document_type':self.document_type,
                    'metadata_options':item,
                })
            self.initial = {1:initial}
        if step == 1:
            self.urldata = []
            for metadata in form.cleaned_data:
                self.urldata.append((metadata['id'],metadata['value']))   

 
    def get_template(self, step):
        return 'generic_wizard.html'

    def done(self, request, form_list):
        url = reverse('upload_document_with_type', args=[self.document_type.id])
        return HttpResponseRedirect('%s?%s' % (url, urlencode(self.urldata)))
