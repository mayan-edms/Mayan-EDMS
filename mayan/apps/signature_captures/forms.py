from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.fields import ImageField
from mayan.apps.views.forms import DetailForm

from .models import SignatureCapture
from .widgets import SignatureCapturesAppWidget


class SignatureCaptureForm(forms.ModelForm):
    class Meta:
        fields = ('data', 'svg', 'text', 'internal_name')
        model = SignatureCapture
        widgets = {
            'data': SignatureCapturesAppWidget(),
            'svg': forms.widgets.HiddenInput(
                attrs={
                    'class': 'signature-captures-capture-svg'
                }
            )
        }


class SignatureCaptureDetailForm(DetailForm):
    preview = ImageField(
        image_alt_text=_('Asset preview image'), label=_('Preview')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['preview'].initial = kwargs['instance']

    class Meta:
        extra_fields = (
            {
                'field': 'date_time_created',
                'widget': forms.widgets.DateTimeInput
            },
            {
                'field': 'date_time_edited',
                'widget': forms.widgets.DateTimeInput
            }
        )
        fields = ('internal_name', 'text', 'user', 'preview')
        model = SignatureCapture
