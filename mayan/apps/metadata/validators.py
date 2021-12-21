import re

from dateutil.parser import parse

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .parsers import MetadataParser


class MetadataValidator(MetadataParser):
    _registry = []

    def validate(self, input_data):
        try:
            self.execute(input_data)
        except Exception as exception:
            raise ValidationError(exception)


class DateAndTimeValidator(MetadataValidator):
    def execute(self, input_data):
        return parse(input_data).isoformat()


class DateValidator(MetadataValidator):
    def execute(self, input_data):
        return parse(input_data).date().isoformat()


class RegularExpressionValidator(MetadataValidator):
    def execute(self, input_data):
        result = re.fullmatch(
            pattern=self.kwargs['pattern'], string=input_data
        )
        if not result:
            raise ValidationError(
                _('The input string does not match the pattern.')
            )
        else:
            return result


class TimeValidator(MetadataValidator):
    def execute(self, input_data):
        return parse(input_data).time().isoformat()


MetadataValidator.register(parser=DateAndTimeValidator)
MetadataValidator.register(parser=DateValidator)
MetadataValidator.register(parser=RegularExpressionValidator)
MetadataValidator.register(parser=TimeValidator)
