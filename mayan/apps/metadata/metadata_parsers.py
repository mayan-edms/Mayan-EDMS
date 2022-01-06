import re

from dateutil.parser import parse

from django.utils.translation import ugettext_lazy as _

from .classes import MetadataParser


class DateAndTimeParser(MetadataParser):
    label = _('Date and time parser')

    def execute(self, input_data):
        return parse(input_data).isoformat()


class DateParser(MetadataParser):
    label = _('Date parser')

    def execute(self, input_data):
        return parse(input_data).date().isoformat()


class RegularExpressionParser(MetadataParser):
    arguments = ('pattern', 'replacement')
    label = _('Regular expression parser')

    def execute(self, input_data):
        return re.sub(
            pattern=self.kwargs['pattern'], repl=self.kwargs['replacement'],
            string=input_data
        )


class TimeParser(MetadataParser):
    label = _('Time parser')

    def execute(self, input_data):
        return parse(input_data).time().isoformat()
