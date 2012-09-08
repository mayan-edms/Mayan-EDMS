from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from smart_settings import LocalScope

from .literals import DEFAULT_LOCK_TIMEOUT_VALUE
from .icons import icon_lock

name = 'lock_manager'
label = _(u'Lock manager')
description = _(u'Handles resource locking.')
icon = icon_lock
dependencies = ['app_registry', 'icons', 'smart_settings']
settings = [
    {
        'name': 'DEFAULT_LOCK_TIMEOUT',
        'default': DEFAULT_LOCK_TIMEOUT_VALUE,
        'description': _(u'Default amount of time in seconds after which a lock will be automatically released.'),
        'scopes': [LocalScope()]
    }
]
