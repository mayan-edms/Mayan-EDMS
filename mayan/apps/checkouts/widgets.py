from __future__ import unicode_literals

import datetime

from django import forms
from django.core import validators
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class SplitDeltaWidget(forms.widgets.MultiWidget):
    """
    A Widget that splits a timedelta input into three <input type="text"> boxes.
    """
    def __init__(self, attrs=None):
        widgets = (
            forms.widgets.TextInput(attrs={'maxlength': 3, 'style': 'width: 5em;', 'placeholder': _('Days')}),
            forms.widgets.TextInput(attrs={'maxlength': 4, 'style': 'width: 5em;', 'placeholder': _('Hours')}),
            forms.widgets.TextInput(attrs={'maxlength': 5, 'style': 'width: 5em;', 'placeholder': _('Minutes')}),
        )
        super(SplitDeltaWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.days, value.seconds / 3600, (value.seconds / 60) % 60]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        return [data.get('expiration_datetime_0', 0) or 0, data.get('expiration_datetime_1', 0) or 0, data.get('expiration_datetime_2', 0) or 0]


class SplitHiddenDeltaWidget(forms.widgets.SplitDateTimeWidget):
    """
    A Widget that splits a timedelta input into three <input type="hidden"> inputs.
    """
    is_hidden = True

    def __init__(self, *args, **kwargs):
        super(SplitHiddenDeltaWidget, self).__init__(*args, **kwargs)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class SplitTimeDeltaField(forms.MultiValueField):
    widget = SplitDeltaWidget
    hidden_widget = SplitHiddenDeltaWidget
    default_error_messages = {
        'invalid_days': _('Enter a valid number of days.'),
        'invalid_hours': _('Enter a valid number of hours.'),
        'invalid_minutes': _('Enter a valid number of minutes.'),
        'invalid_timedelta': _('Enter a valid time difference.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        fields = (
            forms.IntegerField(
                min_value=0,
                error_messages={'invalid': errors['invalid_days']},
                localize=localize
            ),
            forms.IntegerField(
                min_value=0,
                error_messages={'invalid': errors['invalid_hours']},
                localize=localize
            ),
            forms.IntegerField(
                min_value=0,
                error_messages={'invalid': errors['invalid_minutes']},
                localize=localize
            ),
        )
        super(SplitTimeDeltaField, self).__init__(fields, *args, **kwargs)
        self.help_text = _('Amount of time to hold the document in the checked out state in days, hours and/or minutes.')
        self.label = _('Check out expiration date and time')

    def compress(self, data_list):
        if data_list == [0, 0, 0]:
            raise forms.ValidationError(self.error_messages['invalid_timedelta'])

        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_days'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_hours'])
            if data_list[2] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_minutes'])

            timedelta = datetime.timedelta(days=data_list[0], hours=data_list[1], minutes=data_list[2])
            return now() + timedelta
        return None
