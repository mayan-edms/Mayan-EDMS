from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import ModelField, ModelFieldRelated
from mayan.apps.documents.models import Document
from mayan.apps.templating.fields import ModelTemplateField

from .models import SmartLink, SmartLinkCondition


class SmartLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SmartLinkForm, self).__init__(*args, **kwargs)
        self.fields['dynamic_label'] = ModelTemplateField(
            initial_help_text=self.fields['dynamic_label'].help_text,
            label=self.fields['dynamic_label'].label, model=Document,
            model_variable='document', required=False
        )

    class Meta:
        fields = ('label', 'dynamic_label', 'enabled')
        model = SmartLink


class SmartLinkConditionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SmartLinkConditionForm, self).__init__(*args, **kwargs)
        choices = []
        choices.append(
            (
                ModelField.class_label, ModelField.get_choices_for(
                    model=Document,
                )
            )
        )
        choices.append(
            (
                ModelFieldRelated.class_label, ModelFieldRelated.get_choices_for(
                    model=Document,
                )
            )
        )

        self.fields['foreign_document_data'] = forms.ChoiceField(
            choices=choices, label=_('Foreign document field')
        )
        self.fields['expression'] = ModelTemplateField(
            initial_help_text=self.fields['expression'].help_text,
            label=self.fields['expression'].label, model=Document,
            model_variable='document', required=False
        )

    class Meta:
        model = SmartLinkCondition
        exclude = ('smart_link',)
