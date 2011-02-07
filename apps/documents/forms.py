
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from django.core.urlresolvers import reverse

from staging import StagingFile

from common.wizard import BoundFormWizard
from common.utils import urlquote
from common.forms import DetailForm

from models import Document, DocumentType, DocumentTypeMetadataType

from documents.conf.settings import AVAILABLE_FUNCTIONS
from documents.conf.settings import AVAILABLE_MODELS
        
#TODO: Turn this into a base form and let others inherit
class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            if 'document_type' in kwargs['initial']:
                if 'document_type' in self.fields:
                    #To allow merging with DocumentForm_edit
                    self.fields['document_type'].widget = forms.HiddenInput()
                filenames_qs = kwargs['initial']['document_type'].documenttypefilename_set.filter(enabled=True)
                if filenames_qs.count() > 0:
                    self.fields['document_type_available_filenames'] = forms.ModelChoiceField(
                        queryset=filenames_qs,
                        required=False,
                        label=_(u'Document type available filenames'))

    class Meta:
        model = Document


class DocumentForm_view(DetailForm):
    class Meta:
        model = Document
        exclude = ('file',)
        
        
class DocumentForm_edit(DocumentForm):
    class Meta:
        model = Document
        exclude = ('file', 'document_type')
    
    new_filename = forms.CharField(label=_(u'New document filename'), required=False)


class StagingDocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StagingDocumentForm, self).__init__(*args, **kwargs)
        try:
            self.fields['staging_file_id'].choices=[(staging_file.id, staging_file) for staging_file in StagingFile.get_all()]
        except:
            pass
            
        if 'initial' in kwargs:
            if 'document_type' in kwargs['initial']:
                filenames_qs = kwargs['initial']['document_type'].documenttypefilename_set.filter(enabled=True)
                if filenames_qs.count() > 0:
                    self.fields['document_type_available_filenames'] = forms.ModelChoiceField(
                        queryset=filenames_qs,
                        required=False,
                        label=_(u'Document type available filenames'))
            
    staging_file_id = forms.ChoiceField()


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

            if self.metadata_type.lookup:
                try:
                    choices = eval(self.metadata_type.lookup, AVAILABLE_MODELS)
                    self.fields['value'] = forms.ChoiceField(label=self.fields['value'].label)
                    self.fields['value'].choices = zip(choices, choices)
                except Exception, err:
                    self.fields['value'].initial = err
                    self.fields['value'].widget=forms.TextInput(attrs={'readonly':'readonly'})

    id = forms.CharField(label=_(u'id'), widget=forms.HiddenInput)
    name = forms.CharField(label=_(u'Name'),
        required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    value = forms.CharField(label=_(u'Value'))


class DocumentCreateWizard(BoundFormWizard):
    def __init__(self, *args, **kwargs):
        self.multiple = kwargs.pop('multiple', True)
        super(DocumentCreateWizard, self).__init__(*args, **kwargs)
        
    
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
            for id, metadata in enumerate(form.cleaned_data):
                self.urldata.append(('metadata%s_id' % id,metadata['id']))   
                self.urldata.append(('metadata%s_value' % id,metadata['value']))   

 
    def get_template(self, step):
        return 'generic_wizard.html'

    def done(self, request, form_list):
        if self.multiple:
            view = 'upload_multiple_documents_with_type'
        else:
            view = 'upload_document_with_type'

        url = reverse(view, args=[self.document_type.id])
        return HttpResponseRedirect('%s?%s' % (url, urlencode(self.urldata)))
