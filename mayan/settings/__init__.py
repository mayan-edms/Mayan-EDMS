from __future__ import absolute_import

try:
    from .local import *  # NOQA
except ImportError:
    from .base import *  # NOQA
