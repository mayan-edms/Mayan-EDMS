from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from hkp import Key as KeyServerKey

from navigation.api import register_links
from project_setup.api import register_setup

from .api import Key
from .links import (
    key_delete, key_query, key_receive, key_setup, public_keys
)

class DjangoGPGApp(apps.AppConfig):
    name = 'django_gpg'
    verbose_name = _('Django GPG')

    def ready(self):
        register_links(['django_gpg:key_delete', 'django_gpg:key_public_list', 'django_gpg:key_query'], [public_keys, key_query], menu_name='sidebar')
        register_links(Key, [key_delete])
        register_links(KeyServerKey, [key_receive])
        register_setup(key_setup)
