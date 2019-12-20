from __future__ import unicode_literals

from django import forms

from mayan.apps.documents.models import Document
from mayan.apps.templating.fields import TemplateField

from .models import WebLink


class WebLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WebLinkForm, self).__init__(*args, **kwargs)
        self.fields['template'] = TemplateField(
            initial_help_text=self.fields['template'].help_text,
            label=self.fields['template'].label, model=Document,
            model_variable='document', required=True
        )

    class Meta:
        fields = ('label', 'template', 'enabled')
        model = WebLink
