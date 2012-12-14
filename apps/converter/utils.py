from __future__ import absolute_import

import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .settings import GRAPHICS_BACKEND


def _lazy_load(fn):
    _cached = []

    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]
    return _decorated


@_lazy_load
def load_backend():

    try:
        module = import_module('.base', 'converter.backends.%s' % GRAPHICS_BACKEND)
        import warnings
        warnings.warn(
            "Short names for CONVERTER_BACKEND are deprecated; prepend with 'converter.backends.'",
            PendingDeprecationWarning
        )
        return module
    except ImportError, e:
        # Look for a fully qualified converter backend name
        return import_module('.base', backend_name)


def cleanup(filename):
    """
    Tries to remove the given filename. Ignores non-existent files
    """
    try:
        os.remove(filename)
    except OSError:
        pass
