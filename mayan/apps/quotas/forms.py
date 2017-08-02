from __future__ import unicode_literals

import json

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.forms import DynamicModelForm

from .classes import QuotaBackend
from .models import Quota


class QuotaBackendSelectionForm(forms.Form):
    backend = forms.ChoiceField(choices=(), label=_('Backend'))

    def __init__(self, *args, **kwargs):
        super(QuotaBackendSelectionForm, self).__init__(*args, **kwargs)

        self.fields['backend'].choices = QuotaBackend.as_choices()


class QuotaDynamicForm(DynamicModelForm):
    class Meta:
        fields = ('enabled', 'backend_data')
        model = Quota
        widgets = {'backend_data': forms.widgets.HiddenInput}

    def __init__(self, *args, **kwargs):
        result = super(QuotaDynamicForm, self).__init__(*args, **kwargs)
        if self.instance.backend_data:
            for key, value in json.loads(self.instance.backend_data).items():
                self.fields[key].initial = value

        return result

    def clean(self):
        data = super(QuotaDynamicForm, self).clean()

        # Consolidate the dynamic fields into a single JSON field called
        # 'backend_data'.
        backend_data = {}

        for field in self.schema['fields']:
            backend_data[field['name']] = data.pop(
                field['name'], field.get('default', None)
            )

        data['backend_data'] = json.dumps(backend_data)
        return data
