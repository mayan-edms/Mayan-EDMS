import re

from dateutil.parser import parse

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .classes import MetadataValidator


class DateAndTimeValidator(MetadataValidator):
    label = _('Date and time validator')

    def execute(self, input_data):
        parse(input_data).isoformat()


class DateValidator(MetadataValidator):
    label = _('Date validator')

    def execute(self, input_data):
        parse(input_data).date().isoformat()


class RegularExpressionValidator(MetadataValidator):
    arguments = ('pattern',)
    label = _('Regular expression validator')

    def execute(self, input_data):
        result = re.fullmatch(
            pattern=self.kwargs['pattern'], string=input_data
        )
        if not result:
            raise ValidationError(
                _('The input string does not match the pattern.')
            )


class TimeValidator(MetadataValidator):
    label = _('Time validator')

    def execute(self, input_data):
        parse(input_data).time().isoformat()
