from __future__ import absolute_import

from .exceptions import LockError  # NOQA
from .models import Lock as LockModel

Lock = LockModel.objects
