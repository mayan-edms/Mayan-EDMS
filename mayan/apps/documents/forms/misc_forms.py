from django import forms
from django.utils.translation import ugettext_lazy as _

from ..literals import PAGE_RANGE_ALL, PAGE_RANGE_CHOICES


class PrintForm(forms.Form):
    page_group = forms.ChoiceField(
        choices=PAGE_RANGE_CHOICES, initial=PAGE_RANGE_ALL,
        widget=forms.RadioSelect
    )
    page_range = forms.CharField(label=_('Page range'), required=False)


class PageNumberForm(forms.Form):
    page = forms.ModelChoiceField(
        help_text=_(
            'Page number from which all the transformations will be cloned. '
            'Existing transformations will be lost.'
        ), queryset=None
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.fields['page'].queryset = self.instance.pages.all()
