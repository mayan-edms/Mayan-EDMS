from __future__ import unicode_literals

import types

from django.utils import six

if six.PY3:
    dict_type = dict
    dictionary_type = dict
else:
    dict_type = types.DictType
    dictionary_type = types.DictionaryType

try:
    from email.Utils import collapse_rfc2231_value  # NOQA
except ImportError:
    from email.utils import collapse_rfc2231_value  # NOQA

try:
    FileNotFoundError
except NameError:
    FileNotFoundErrorException = IOError
else:
    FileNotFoundErrorException = FileNotFoundError  # NOQA
