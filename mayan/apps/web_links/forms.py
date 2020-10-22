from django import forms
from django.utils.text import format_lazy

from mayan.apps.documents.models import Document
from mayan.apps.templating.fields import ModelTemplateField

from .models import WebLink


class WebLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['template'] = ModelTemplateField(
            initial_help_text=format_lazy(
                '{} ', self.fields['template'].help_text
            ), label=self.fields['template'].label, model=Document,
            model_variable='document', required=True
        )

    class Meta:
        fields = ('label', 'template', 'enabled')
        model = WebLink
