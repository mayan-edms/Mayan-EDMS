from __future__ import unicode_literals

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.classes import ModelField, ModelProperty
from mayan.apps.documents.models import Document

from .models import SmartLink, SmartLinkCondition


class SmartLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SmartLinkForm, self).__init__(*args, **kwargs)
        self.fields['dynamic_label'].help_text = ' '.join(
            [
                force_text(self.fields['dynamic_label'].help_text),
                ModelProperty.get_help_text_for(
                    model=Document, show_name=True
                ).replace('\n', '<br>')
            ]
        )

    class Meta:
        fields = ('label', 'dynamic_label', 'enabled')
        model = SmartLink


class SmartLinkConditionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SmartLinkConditionForm, self).__init__(*args, **kwargs)
        self.fields['foreign_document_data'] = forms.ChoiceField(
            choices=ModelField.get_choices_for(
                model=Document,
            ), label=_('Foreign document field')
        )
        self.fields['expression'].help_text = ' '.join(
            [
                force_text(self.fields['expression'].help_text),
                ModelProperty.get_help_text_for(
                    model=Document, show_name=True
                ).replace('\n', '<br>')
            ]
        )

    class Meta:
        model = SmartLinkCondition
        exclude = ('smart_link',)
