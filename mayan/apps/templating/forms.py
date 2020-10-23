from django import forms
from django.utils.translation import ugettext_lazy as _

from .fields import ModelTemplateField


class DocumentTemplateSandboxForm(forms.Form):
    result = forms.CharField(
        help_text=_('Resulting text from the evaluated template.'),
        label=_('Result'), required=False, widget=forms.widgets.Textarea(
            attrs={'readonly': 'readonly', 'rows': 5}
        )
    )

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.model_variable = kwargs.pop('model_variable')
        super(DocumentTemplateSandboxForm, self).__init__(*args, **kwargs)
        self.fields['template'] = ModelTemplateField(
            initial_help_text=_('The template string to be evaluated.'),
            label=_('Template'), model=self.model,
            model_variable=self.model_variable, required=True
        )
        self.order_fields(field_order=('template', 'result'))
