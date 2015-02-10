try:
    from .local import *  # NOQA
except ImportError:
    from .base import *  # NOQA
