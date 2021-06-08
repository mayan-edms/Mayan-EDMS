from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.templating.fields import TemplateField
from mayan.apps.views.forms import RelationshipForm

from .classes import MetadataLookup
from .models import MetadataType


class DocumentMetadataForm(forms.Form):
    metadata_type_id = forms.CharField(label=_('ID'), widget=forms.HiddenInput)
    metadata_type_name = forms.CharField(
        label=_('Name'), required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    value = forms.CharField(
        label=_('Value'), required=False, widget=forms.TextInput(
            attrs={'class': 'metadata-value'}
        )
    )
    update = forms.BooleanField(
        initial=True, label=_('Update'), required=False
    )

    class Media:
        js = ('metadata/js/metadata_form.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set form fields initial values
        if 'initial' in kwargs:
            self.metadata_type = kwargs['initial']['metadata_type']
            self.document_type = kwargs['initial']['document_type']
            required_string = ''

            required = self.metadata_type.get_required_for(
                document_type=self.document_type
            )

            if required:
                self.fields['value'].required = True
                required_string = ' (%s)' % _('Required')
            else:
                self.fields['value'].required = False
                self.fields['update'].initial = False

            self.fields['metadata_type_name'].initial = '%s%s' % (
                (
                    self.metadata_type.label if self.metadata_type.label else self.metadata_type.name
                ),
                required_string
            )
            self.fields['metadata_type_id'].initial = self.metadata_type.pk

            if self.metadata_type.lookup:
                try:
                    self.fields['value'] = forms.ChoiceField(
                        label=self.fields['value'].label
                    )
                    choices = self.metadata_type.get_lookup_values()
                    choices = list(zip(choices, choices))
                    if not required:
                        choices.insert(0, ('', '------'))
                    self.fields['value'].choices = choices
                    self.fields['value'].required = required
                    self.fields['value'].widget.attrs.update(
                        {'class': 'metadata-value'}
                    )
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

    def clean(self):
        metadata_type = getattr(self, 'metadata_type', None)

        if metadata_type:
            required = self.metadata_type.get_required_for(
                document_type=self.document_type
            )

            # Enforce required only if the metadata has no previous value.
            if required and not self.cleaned_data.get('value') and not self.cleaned_data.get('update'):
                raise ValidationError(
                    _(
                        '"%s" is required for this document type.'
                    ) % self.metadata_type.label
                )

        if self.cleaned_data.get('update') and hasattr(self, 'metadata_type'):
            self.cleaned_data['value'] = self.metadata_type.validate_value(
                document_type=self.document_type,
                value=self.cleaned_data.get('value')
            )

        return self.cleaned_data


DocumentMetadataFormSet = formset_factory(form=DocumentMetadataForm, extra=0)


class DocumentMetadataAddForm(forms.Form):
    metadata_type = forms.ModelMultipleChoiceField(
        help_text=_('Metadata types to be added to the selected documents.'),
        label=_('Metadata type'), queryset=MetadataType.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'select2'},
        )
    )

    def __init__(self, *args, **kwargs):
        document_type = kwargs.pop('document_type', None)

        if document_type:
            queryset = kwargs.pop(
                'queryset', MetadataType.objects.get_for_document_type(
                    document_type=document_type
                )
            )
        else:
            queryset = MetadataType.objects.none()

        super().__init__(*args, **kwargs)

        self.fields['metadata_type'].queryset = queryset


class DocumentMetadataRemoveForm(DocumentMetadataForm):
    update = forms.BooleanField(
        initial=False, label=_('Remove'), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('value')

    def clean(self):
        return super(forms.Form, self).clean()


DocumentMetadataRemoveFormSet = formset_factory(
    form=DocumentMetadataRemoveForm, extra=0
)


class MetadataTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default'] = TemplateField(
            initial_help_text=self.fields['default'].help_text, required=False
        )
        self.fields['lookup'] = TemplateField(
            initial_help_text=format_lazy(
                '{}{}{}',
                self.fields['lookup'].help_text,
                _(' Available template context variables: '),
                MetadataLookup.get_as_help_text()
            ), required=False
        )

    class Meta:
        fields = ('name', 'label', 'default', 'lookup', 'validation', 'parser')
        model = MetadataType


class DocumentTypeMetadataTypeRelationshipForm(RelationshipForm):
    RELATIONSHIP_TYPE_NONE = 'none'
    RELATIONSHIP_TYPE_OPTIONAL = 'optional'
    RELATIONSHIP_TYPE_REQUIRED = 'required'
    RELATIONSHIP_CHOICES = (
        (RELATIONSHIP_TYPE_NONE, _('None')),
        (RELATIONSHIP_TYPE_OPTIONAL, _('Optional')),
        (RELATIONSHIP_TYPE_REQUIRED, _('Required')),
    )

    def get_relationship_type(self):
        relationship_queryset = self.get_relationship_queryset()

        if relationship_queryset.exists():
            if relationship_queryset.get().required:
                return self.RELATIONSHIP_TYPE_REQUIRED
            else:
                return self.RELATIONSHIP_TYPE_OPTIONAL
        else:
            return self.RELATIONSHIP_TYPE_NONE

    def save_relationship_none(self):
        instance = self.get_relationship_instance()
        instance._event_actor = self._event_actor
        instance.delete()

    def save_relationship_optional(self):
        instance = self.get_relationship_instance()
        instance.required = False
        instance._event_actor = self._event_actor
        instance.save()

    def save_relationship_required(self):
        instance = self.get_relationship_instance()
        instance.required = True
        instance._event_actor = self._event_actor
        instance.save()


DocumentTypeMetadataTypeRelationshipFormSetBase = formset_factory(
    form=DocumentTypeMetadataTypeRelationshipForm, extra=0
)


class DocumentTypeMetadataTypeRelationshipFormSet(DocumentTypeMetadataTypeRelationshipFormSetBase):
    def __init__(self, *args, **kwargs):
        _event_actor = kwargs.pop('_event_actor')
        super().__init__(*args, **kwargs)
        self.form_kwargs.update({'_event_actor': _event_actor})
