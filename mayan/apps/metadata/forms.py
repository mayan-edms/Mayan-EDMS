from __future__ import absolute_import

from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import ugettext_lazy as _

from .models import MetadataType
from .settings import AVAILABLE_FUNCTIONS, AVAILABLE_MODELS, AVAILABLE_VALIDATORS


class MetadataForm(forms.Form):

    def clean_value(self):
        value = self.cleaned_data['value']
        metadata_id = self.cleaned_data['id']
        metadata_type = MetadataType.objects.get(pk=metadata_id)
        if metadata_type.lookup and metadata_type.lookup in AVAILABLE_VALIDATORS:
            val_func = AVAILABLE_VALIDATORS[metadata_type.lookup]
            new_value = val_func(value)
            if new_value:
                value = new_value
        return value

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs)

        # Set form fields initial values
        if 'initial' in kwargs:
            self.metadata_type = kwargs['initial'].pop('metadata_type', None)
            required = kwargs['initial'].pop('required', False)
            required_string = u''

            if required:
                self.fields['value'].required = True
                required_string = u' (%s)' % _('Required')
            else:
                self.fields['value'].required = False

            self.fields['name'].initial = '%s%s' % ((self.metadata_type.title if self.metadata_type.title else self.metadata_type.name), required_string)
            self.fields['id'].initial = self.metadata_type.pk

            if self.metadata_type.lookup and self.metadata_type.lookup not in AVAILABLE_VALIDATORS:
                try:
                    choices = eval(self.metadata_type.lookup, AVAILABLE_MODELS)
                    self.fields['value'] = forms.ChoiceField(label=self.fields['value'].label)
                    choices = zip(choices, choices)
                    if not required:
                        choices.insert(0, ('', '------'))
                    self.fields['value'].choices = choices
                    self.fields['value'].required = required
                except Exception as exception:
                    self.fields['value'].initial = exception
                    self.fields['value'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

            if self.metadata_type.default:
                try:
                    self.fields['value'].initial = eval(self.metadata_type.default, AVAILABLE_FUNCTIONS)
                except Exception as exception:
                    self.fields['value'].initial = exception

    id = forms.CharField(label=_(u'ID'), widget=forms.HiddenInput)

    name = forms.CharField(label=_(u'Name'), required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    value = forms.CharField(label=_(u'Value'), required=False)
    update = forms.BooleanField(initial=True, label=_(u'Update'), required=False)

MetadataFormSet = formset_factory(MetadataForm, extra=0)


class AddMetadataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type')
        super(AddMetadataForm, self).__init__(*args, **kwargs)
        self.fields['metadata_type'].queryset = document_type.metadata.all()

    metadata_type = forms.ModelChoiceField(queryset=MetadataType.objects.all(), label=_(u'Metadata type'))


class MetadataRemoveForm(MetadataForm):
    update = forms.BooleanField(initial=False, label=_(u'Remove'), required=False)


MetadataRemoveFormSet = formset_factory(MetadataRemoveForm, extra=0)


class MetadataTypeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'title', 'default', 'lookup')
        model = MetadataType
