from __future__ import unicode_literals

from .exceptions import LockError  # NOQA
from .models import Lock as LockModel

Lock = LockModel.objects
default_app_config = 'lock_manager.apps.LockManagerApp'
