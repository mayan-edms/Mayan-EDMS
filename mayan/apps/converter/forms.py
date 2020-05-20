import yaml

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_load

from .models import LayerTransformation
from .transformations import BaseTransformation


class LayerTransformationSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        layer = kwargs.pop('layer')
        super(LayerTransformationSelectForm, self).__init__(*args, **kwargs)
        self.fields[
            'transformation'
        ].choices = BaseTransformation.get_transformation_choices(layer=layer)

    transformation = forms.ChoiceField(
        choices=(), help_text=_('Available transformations for this layer.'),
        label=_('Transformation'),
    )


class LayerTransformationForm(forms.ModelForm):
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
