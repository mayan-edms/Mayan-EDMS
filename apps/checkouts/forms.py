from __future__ import absolute_import

import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import DocumentCheckout


class SplitDateTimeWidget(forms.widgets.MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    """
    date_format = forms.widgets.DateInput.format
    time_format = forms.widgets.TimeInput.format

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.widgets.DateInput(attrs=attrs, format=date_format),
                   forms.widgets.TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

class SplitHiddenDateTimeWidget(forms.widgets.SplitDateTimeWidget):
    """
    A Widget that splits datetime input into two <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(SplitHiddenDateTimeWidget, self).__init__(attrs, date_format, time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class SplitTimeDeltaField(forms.MultiValueField):
    widget = SplitDateTimeWidget
    hidden_widget = SplitHiddenDateTimeWidget
    default_error_messages = {
        'invalid_date': _(u'Enter a valid date.'),
        'invalid_time': _(u'Enter a valid time.'),
    }

    def __init__(self, input_date_formats=None, input_time_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            forms.DateField(input_formats=input_date_formats,
                      error_messages={'invalid': errors['invalid_date']},
                      localize=localize),
            forms.TimeField(input_formats=input_time_formats,
                      error_messages={'invalid': errors['invalid_time']},
                      localize=localize),
        )
        super(SplitTimeDeltaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None


class DocumentCheckoutForm(forms.ModelForm):
    days = forms.IntegerField(min_value=0, label=_(u'Days'), help_text=_(u'Amount of time to hold the document checked out in days.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 3, 'style':'width: 5em;'}))
    hours = forms.IntegerField(min_value=0, label=_(u'Hours'), help_text=_(u'Amount of time to hold the document checked out in hours.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 4, 'style':'width: 5em;'}))
    minutes = forms.IntegerField(min_value=0, label=_(u'Minutes'), help_text=_(u'Amount of time to hold the document checked out in minutes.'), required=False, widget=forms.widgets.TextInput(attrs={'maxlength': 5, 'style':'width: 5em;'}))

    expiration_datetime = SplitTimeDeltaField()
    class Meta:
        model = DocumentCheckout
        widgets = {
            'document': forms.widgets.HiddenInput(),
        }

       
