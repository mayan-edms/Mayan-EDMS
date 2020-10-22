import json

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import DynamicModelForm

from .classes import QuotaBackend
from .models import Quota


class QuotaBackendSelectionForm(forms.Form):
    backend = forms.ChoiceField(
        choices=(), label=_('Backend'), help_text=_(
            'The quota driver for this entry.'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = QuotaBackend.as_choices()


class QuotaDynamicForm(DynamicModelForm):
    class Meta:
        fields = ('enabled', 'backend_data')
        model = Quota
        widgets = {'backend_data': forms.widgets.HiddenInput}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', {})
        result = super().__init__(*args, **kwargs)

        # Handle filtered queryset fields
        for field in self.fields:
            if hasattr(self.fields[field], 'reload'):
                self.fields[field].user = self.user
                self.fields[field].reload()

        if self.instance.backend_data:
            for key, value in json.loads(s=self.instance.backend_data).items():
                self.fields[key].initial = value

        return result

    def clean(self):
        data = super().clean()
        # Consolidate the dynamic fields into a single JSON field called
        # 'backend_data'.
        backend_data = {}

        for field_name, field_data in self.schema['fields'].items():
            field_data = data.pop(
                field_name, field_data.get('default', None)
            )

            # Reduce models to a pk
            if isinstance(field_data, models.Model):
                field_data = field_data.pk

            # Reduce querysets to a list
            if isinstance(field_data, models.query.QuerySet):
                field_data = list(field_data.values_list('pk', flat=True))

            backend_data[field_name] = field_data

        data['backend_data'] = json.dumps(obj=backend_data)
        return data
