import json
import re
import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import six
from django.utils.deconstruct import deconstructible
from django.utils.functional import SimpleLazyObject
from django.utils.translation import ugettext_lazy as _

# These values, if given to validate(), will trigger the self.required check.
EMPTY_VALUES = (None, '', [], (), {})


def _lazy_re_compile(regex, flags=0):
    """Lazily compile a regex with flags."""
    def _compile():
        # Compile the regex if it was not passed pre-compiled.
        if isinstance(regex, six.string_types):
            return re.compile(regex, flags)
        else:
            assert not flags, 'flags must be empty if regex is passed pre-compiled'
            return regex
    return SimpleLazyObject(_compile)


@deconstructible
class JSONValidator(object):
    """
    Validates that the input is JSON compliant.
    """
    def __call__(self, value):
        value = value.strip()
        try:
            json.loads(s=value)
        except ValueError:
            raise ValidationError(
                _('Enter a valid JSON value.'),
                code='invalid'
            )

    def __eq__(self, other):
        return (
            isinstance(other, JSONValidator)
        )

    def __ne__(self, other):
        return not (self == other)


@deconstructible
class YAMLValidator(object):
    """
    Validates that the input is YAML compliant.
    """
    def __call__(self, value):
        value = value.strip()
        try:
            yaml.load(stream=value, Loader=SafeLoader)
        except yaml.error.YAMLError:
            raise ValidationError(
                _('Enter a valid YAML value.'),
                code='invalid'
            )

    def __eq__(self, other):
        return (
            isinstance(other, YAMLValidator)
        )

    def __ne__(self, other):
        return not (self == other)


internal_name_re = _lazy_re_compile(r'^[a-zA-Z0-9_]+\Z')
validate_internal_name = RegexValidator(
    internal_name_re, _(
        "Enter a valid 'internal name' consisting of letters, numbers, and "
        "underscores."
    ), 'invalid'
)
