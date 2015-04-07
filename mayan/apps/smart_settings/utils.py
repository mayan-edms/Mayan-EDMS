from __future__ import unicode_literals

import types


def return_type(value):
    if isinstance(value, types.FunctionType):
        return value.__doc__ if value.__doc__ else _('Function found')
    elif isinstance(value, types.ClassType):
        return '%s.%s' % (value.__class__.__module__, value.__class__.__name__)
    elif isinstance(value, types.TypeType):
        return '%s.%s' % (value.__module__, value.__name__)
    elif isinstance(value, types.DictType) or isinstance(value, types.DictionaryType):
        return ', '.join(list(value))
    else:
        return value
