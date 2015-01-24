from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace='django_gpg',
    module='django_gpg.settings',
    settings=[
        {'name': 'KEYSERVERS', 'global_name': 'SIGNATURES_KEYSERVERS', 'default': ['pool.sks-keyservers.net'], 'description': _('List of keyservers to be queried for unknown keys.')},
        {'name': 'GPG_HOME', 'global_name': 'SIGNATURES_GPG_HOME', 'default': os.path.join(settings.MEDIA_ROOT, 'gpg_home'), 'description': _('Home directory used to store keys as well as configuration files.')},
        {'name': 'GPG_PATH', 'global_name': 'SIGNATURES_GPG_PATH', 'default': '/usr/bin/gpg', 'exists': True, 'description': _('Path to the GPG binary.')},
    ]
)
