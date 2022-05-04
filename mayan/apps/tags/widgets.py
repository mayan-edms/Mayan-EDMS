from django import forms
from django.utils.html import conditional_escape


class ColorWidget(forms.TextInput):
    template_name = 'tags/widget_tag_color.html'

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['type'] = 'color'
        super().__init__(attrs=attrs)


class TagFormWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        result = super().create_option(
            attrs=attrs, index=index,
            label='{}'.format(conditional_escape(label)), name=name,
            selected=selected, subindex=subindex, value=value
        )

        result['attrs']['data-color'] = value.instance.color

        return result
