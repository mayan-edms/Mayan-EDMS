try:
    # Python 3.10
    from collections.abc import Iterable
except ImportError:
    # Python < 3.10
    from collections import Iterable  # NOQA: F401
