from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.forms import DetailForm

from .literals import STATE_LABELS
from .models import DocumentCheckout
from .widgets import SplitTimeDeltaWidget


class DocumentCheckOutForm(forms.ModelForm):
    class Meta:
        fields = ('expiration_datetime', 'block_new_file')
        model = DocumentCheckout
        widgets = {
            'expiration_datetime': SplitTimeDeltaWidget()
        }


class DocumentCheckOutDetailForm(DetailForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance']

        extra_fields = (
            {
                'label': _('Document status'),
                'field': lambda instance: STATE_LABELS[
                    instance.get_check_out_state()
                ]
            },
        )

        if instance.is_checked_out():
            checkout_info = instance.get_check_out_info()
            extra_fields += (
                {
                    'label': _('User'),
                    'field': lambda instance: checkout_info.user.get_full_name() or checkout_info.user
                },
                {
                    'label': _('Check out time'),
                    'field': lambda instance: checkout_info.checkout_datetime,
                    'widget': forms.widgets.DateTimeInput
                },
                {
                    'label': _('Check out expiration'),
                    'field': lambda instance: checkout_info.expiration_datetime,
                    'widget': forms.widgets.DateTimeInput
                },
                {
                    'label': _('New files allowed?'),
                    'field': lambda instance: _('Yes') if not checkout_info.block_new_file else _('No')
                },
            )

        kwargs['extra_fields'] = extra_fields
        super().__init__(*args, **kwargs)

    class Meta:
        fields = ()
        model = DocumentCheckout
