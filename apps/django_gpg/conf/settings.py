"""
Configuration options for the django_gpg app
"""
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from smart_settings.api import Setting, SettingNamespace

namespace = SettingNamespace('django_gpg', _(u'Signatures'), module='django_gpg.conf.settings', sprite='text_signature')

Setting(
    namespace=namespace,
    name='KEYSERVERS',
    global_name='SIGNATURES_KEYSERVERS',
    default=['pool.sks-keyservers.net'],
    description=_(u'List of keyservers to be queried for unknown keys.'),
)

Setting(
    namespace=namespace,
    name='GPG_HOME',
    global_name='SIGNATURES_GPG_HOME',
    default=os.path.join(settings.PROJECT_ROOT, u'gpg_home'),
    description=_(u'Home directory used to store keys as well as configuration files.'),
    exists=True,
)
