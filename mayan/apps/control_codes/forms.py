from __future__ import unicode_literals

import yaml

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.forms import DetailForm
from mayan.apps.common.serialization import yaml_load

from .classes import ControlCode
from .models import ControlSheet, ControlSheetCode


class ControlCodeClassSelectionForm(forms.Form):
    control_code = forms.ChoiceField(
        choices=(), help_text=_('Available control codes.'),
        label=_('Control code'),
    )

    def __init__(self, *args, **kwargs):
        super(ControlCodeClassSelectionForm, self).__init__(*args, **kwargs)

        self.fields[
            'control_code'
        ].choices = ControlCode.get_choices()

"""
class ControlSheetDetailForm(DetailForm):
    '''
    def __init__(self, *args, **kwargs):
        document = kwargs['instance']

        extra_fields = [
            {
                'label': _('Date added'),
                'field': 'date_added',
                'widget': forms.widgets.DateTimeInput
            },
            {'label': _('UUID'), 'field': 'uuid'},
            {
                'label': _('Language'),
                'field': lambda x: get_language(language_code=document.language)
            },
        ]

        if document.latest_version:
            extra_fields += (
                {
                    'label': _('File mimetype'),
                    'field': lambda x: document.file_mimetype or _('None')
                },
                {
                    'label': _('File encoding'),
                    'field': lambda x: document.file_mime_encoding or _(
                        'None'
                    )
                },
                {
                    'label': _('File size'),
                    'field': lambda document: filesizeformat(
                        document.size
                    ) if document.size else '-'
                },
                {'label': _('Exists in storage'), 'field': 'exists'},
                {
                    'label': _('File path in storage'),
                    'field': 'latest_version.file'
                },
                {'label': _('Checksum'), 'field': 'checksum'},
                {'label': _('Pages'), 'field': 'page_count'},
            )

        kwargs['extra_fields'] = extra_fields
        super(DocumentPropertiesForm, self).__init__(*args, **kwargs)
    '''
    class Meta:
        fields = ('label', 'codes')
        model = ControlSheet

"""

"""
class ControlSheetCodeForm(forms.ModelForm):
    class Meta:
        fields = ('arguments', 'order')
        model = LayerTransformation

    def __init__(self, *args, **kwargs):
        transformation_name = kwargs.pop('transformation_name', None)
        super(LayerTransformationForm, self).__init__(*args, **kwargs)

        if not transformation_name:
            # Get the template name when the transformation is being edited.
            template_name = getattr(
                self.instance.get_transformation_class(), 'template_name',
                None
            )
        else:
            # Get the template name when the transformation is being created
            template_name = getattr(
                BaseTransformation.get(name=transformation_name),
                'template_name', None
            )

        if template_name:
            self.fields['arguments'].widget.attrs['class'] = 'hidden'
            self.fields['order'].widget.attrs['class'] = 'hidden'

    def clean(self):
        try:
            yaml_load(stream=self.cleaned_data['arguments'])
        except yaml.YAMLError:
            raise ValidationError(
                _(
                    '"%s" not a valid entry.'
                ) % self.cleaned_data['arguments']
            )
"""
