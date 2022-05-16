import yaml

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.serialization import yaml_dump, yaml_load
from mayan.apps.views.forms import DetailForm, ModelForm

from .fields import ImageField
from .models import Asset, LayerTransformation
from .transformations import BaseTransformation


class AssetDetailForm(DetailForm):
    preview = ImageField(
        image_alt_text=_('Asset preview image'), label=_('Preview')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preview'].initial = kwargs['instance']

    class Meta:
        fields = ('label', 'internal_name', 'preview')
        model = Asset


class LayerTransformationSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        layer = kwargs.pop('layer')
        super().__init__(*args, **kwargs)
        self.fields[
            'transformation'
        ].choices = BaseTransformation.get_transformation_choices(layer=layer)

    transformation = forms.ChoiceField(
        choices=(), help_text=_('Available transformations for this layer.'),
        label=_('Transformation')
    )


class LayerTransformationForm(ModelForm):
    class Meta:
        fields = ('arguments', 'order')
        model = LayerTransformation

    def __init__(self, *args, **kwargs):
        self._transformation_name = kwargs.pop('transformation_name', None)

        super().__init__(*args, **kwargs)
        transformation_class = self.get_transformation_class()
        if self.instance:
            for key, value in yaml_load(stream=self.instance.arguments or '{}').items():
                self.initial[key] = value

        self.template_name = getattr(
            transformation_class, 'template_name', None
        )

        if self.template_name:
            self.fields['arguments'].widget.attrs['class'] = 'hidden'
            self.fields['order'].widget.attrs['class'] = 'hidden'
        else:
            self.fields['arguments'].widget = forms.widgets.HiddenInput()

    def get_transformation_class(self):
        if not self._transformation_name:
            return self.instance.get_transformation_class()
        else:
            return BaseTransformation.get(name=self._transformation_name)

    def clean(self):
        if self.template_name:
            # If the transformation specifies a template, take the values
            # provided and just check for valid format.
            # Allows compatibility with the redaction template and
            # JavaScript.
            try:
                yaml_load(stream=self.cleaned_data['arguments'])
            except yaml.YAMLError:
                raise ValidationError(
                    _(
                        '"%s" not a valid entry.'
                    ) % self.cleaned_data['arguments']
                )
        else:
            # Otherwise grab the values from the dynamic form and create
            # the argument JSON object.
            arguments = {}

            for argument in self.get_transformation_class().get_arguments():
                if self.cleaned_data[argument] is not None:
                    arguments[argument] = self.cleaned_data[argument]

            self.cleaned_data['arguments'] = yaml_dump(data=arguments)
