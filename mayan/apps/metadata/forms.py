from __future__ import unicode_literals

import shlex

from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.template import Context, Template
from django.utils.module_loading import import_string
from django.utils.translation import string_concat, ugettext_lazy as _

from .classes import MetadataLookup
from .models import MetadataType


class MetadataForm(forms.Form):
    @staticmethod
    def comma_splitter(string):
        splitter = shlex.shlex(string.encode('utf-8'), posix=True)
        splitter.whitespace = ','.encode('utf-8')
        splitter.whitespace_split = True
        splitter.commenters = ''.encode('utf-8')
        return list(splitter)

    def clean_value(self):
        metadata_type = MetadataType.objects.get(pk=self.cleaned_data['id'])

        if metadata_type.validation:
            validator = import_string(metadata_type.validation)()

            try:
                # If it is a parsing function we should get a value
                # If it is a validation function we get nothing on success
                result = validator.validate(self.cleaned_data['value'])
            except Exception as exception:
                # If it is a validation function and an exception is raise
                # we wrap that into a new ValidationError exception
                # If the function exception is a ValidationError itself the
                # error messages will be in a 'messages' property, so we
                # contatenate them.
                # Otherwise we extract whatever single message the exception
                # included.
                try:
                    message = ', '.join(exception.messages)
                except AttributeError:
                    message = unicode(exception)

                raise ValidationError(
                    _('Invalid value: %(message)s'), params={
                        'message': message
                    }, code='invalid'
                )
            else:
                # Return the result if it was a parsing function
                # If it was a validation function and passed correctly
                # we return the original input value
                return result or self.cleaned_data['value']
        else:
            # If a validator was never specified we return the original
            # value
            return self.cleaned_data['value']

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs)

        # Set form fields initial values
        if 'initial' in kwargs:
            self.metadata_type = kwargs['initial'].pop('metadata_type', None)
            required = kwargs['initial'].pop('required', False)
            required_string = ''

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
                    template = Template(self.metadata_type.lookup)
                    context = Context(MetadataLookup.get_as_context())
                    choices = MetadataForm.comma_splitter(
                        template.render(context=context)
                    )
                    self.fields['value'] = forms.ChoiceField(
                        label=self.fields['value'].label
                    )
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
                    template = Template(self.metadata_type.default)
                    context = Context()
                    result = template.render(context=context)
                    self.fields['value'].initial = result
                except Exception as exception:
                    self.fields['value'].initial = _(
                        'Default value error: %s'
                    ) % exception
                    self.fields['value'].widget = forms.TextInput(
                        attrs={'readonly': 'readonly'}
                    )

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
        fields = ('name', 'label', 'default', 'lookup', 'validation')
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
