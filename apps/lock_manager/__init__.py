from __future__ import absolute_import

import logging

from .exceptions import LockError
from .models import Lock as LockModel

logger = logging.getLogger(__name__)

Lock = LockModel.objects
