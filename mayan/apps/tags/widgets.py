from django import forms
from django.utils.html import conditional_escape


class TagFormWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        result = super().create_option(
            attrs=attrs, index=index,
            label='{}'.format(conditional_escape(label)), name=name,
            selected=selected, subindex=subindex, value=value
        )

        result['attrs']['data-color'] = self.choices.queryset.get(pk=value).color

        return result
