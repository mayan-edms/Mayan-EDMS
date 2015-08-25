from __future__ import unicode_literals

from django import forms
from django.forms.formsets import formset_factory
from django.utils.translation import string_concat, ugettext_lazy as _

from .classes import MetadataLookup
from .models import MetadataType


class MetadataForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs)

        # Set form fields initial values
        if 'initial' in kwargs:
            self.metadata_type = kwargs['initial'].pop('metadata_type', None)
            self.document_type = kwargs['initial'].pop('document_type', None)
            required_string = ''

            required = self.metadata_type.get_required_for(document_type=self.document_type)
            if required:
                self.fields['value'].required = True
                required_string = ' (%s)' % _('Required')
            else:
                self.fields['value'].required = False

            self.fields['name'].initial = '%s%s' % (
                (
                    self.metadata_type.label if self.metadata_type.label else self.metadata_type.name
                ),
                required_string
            )
            self.fields['id'].initial = self.metadata_type.pk

            if self.metadata_type.lookup:
                try:
                    self.fields['value'] = forms.ChoiceField(
                        label=self.fields['value'].label
                    )
                    choices = self.metadata_type.get_lookup_values()
                    choices = zip(choices, choices)
                    if not required:
                        choices.insert(0, ('', '------'))
                    self.fields['value'].choices = choices
                    self.fields['value'].required = required
                except Exception as exception:
                    self.fields['value'].initial = _(
                        'Lookup value error: %s'
                    ) % exception
                    self.fields['value'].widget = forms.TextInput(
                        attrs={'readonly': 'readonly'}
                    )

            if self.metadata_type.default:
                try:
                    self.fields[
                        'value'
                    ].initial = self.metadata_type.get_default_value()
                except Exception as exception:
                    self.fields['value'].initial = _(
                        'Default value error: %s'
                    ) % exception
                    self.fields['value'].widget = forms.TextInput(
                        attrs={'readonly': 'readonly'}
                    )

    def clean_value(self):
        return self.metadata_type.validate_value(document_type=self.document_type, value=self.cleaned_data['value'])

    id = forms.CharField(label=_('ID'), widget=forms.HiddenInput)

    name = forms.CharField(
        label=_('Name'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    value = forms.CharField(label=_('Value'), required=False)
    update = forms.BooleanField(
        initial=True, label=_('Update'), required=False
    )

MetadataFormSet = formset_factory(MetadataForm, extra=0)


class AddMetadataForm(forms.Form):
    metadata_type = forms.ModelChoiceField(
        queryset=MetadataType.objects.all(), label=_('Metadata type')
    )

    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type')
        super(AddMetadataForm, self).__init__(*args, **kwargs)
        self.fields['metadata_type'].queryset = document_type.metadata.all()


class MetadataTypeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'label', 'default', 'lookup', 'validation', 'parser')
        model = MetadataType

    def __init__(self, *args, **kwargs):
        super(MetadataTypeForm, self).__init__(*args, **kwargs)
        self.fields['lookup'].help_text = string_concat(
            self.fields['lookup'].help_text,
            _(' Available template context variables: '),
            MetadataLookup.get_as_help_text()
        )


class MetadataRemoveForm(MetadataForm):
    update = forms.BooleanField(
        initial=False, label=_('Remove'), required=False
    )

    def __init__(self, *args, **kwargs):
        super(MetadataRemoveForm, self).__init__(*args, **kwargs)
        self.fields.pop('value')


MetadataRemoveFormSet = formset_factory(MetadataRemoveForm, extra=0)
