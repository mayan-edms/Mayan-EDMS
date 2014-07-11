"""
Configuration options for the django_gpg app
"""
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from smart_settings.api import register_settings

register_settings(
    namespace=u'django_gpg',
    module=u'django_gpg.conf.settings',
    settings=[
        {'name': u'KEYSERVERS', 'global_name': u'SIGNATURES_KEYSERVERS', 'default': ['pool.sks-keyservers.net'], 'description': _(u'List of keyservers to be queried for unknown keys.')},
        {'name': u'GPG_HOME', 'global_name': u'SIGNATURES_GPG_HOME', 'default': os.path.join(settings.MEDIA_ROOT, u'gpg_home'), 'description': _(u'Home directory used to store keys as well as configuration files.')},
    ]
)
