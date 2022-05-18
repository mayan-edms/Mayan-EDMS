from django import forms as django_forms

from mayan.apps.views.forms import Form

from ..classes import Layer
from ..forms import LayerTransformationForm


class DynamicTransformationFormClassMixin:
    def get_form_class(self):
        transformation_class = self.get_transformation_class()

        TransformationForm = transformation_class.get_form_class()

        if not TransformationForm and not getattr(transformation_class, 'template_name', None):
            # Transformation does not specify a form and does not have
            # a template either. Create a dynamic form based on the argument
            # list.
            class TransformationForm(Form):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    for argument in transformation_class.get_arguments():
                        self.fields[argument] = django_forms.CharField(required=False)

        class MergedTransformationForm(
            TransformationForm, LayerTransformationForm
        ):
            """Model form merged with the specific transformation fields."""
            view = self

        return MergedTransformationForm


class LayerViewMixin:
    def dispatch(self, request, *args, **kwargs):
        self.layer = self.get_layer()
        return super().dispatch(request=request, *args, **kwargs)

    def get_layer(self):
        return Layer.get(
            name=self.kwargs['layer_name']
        )
