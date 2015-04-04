from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _

from hkp import Key as KeyServerKey

from common import menu_setup

from .api import Key
from .links import (
    key_delete, key_query, key_receive, link_key_setup, public_keys
)


class DjangoGPGApp(apps.AppConfig):
    name = 'django_gpg'
    verbose_name = _('Django GPG')

    def ready(self):
        # TODO: convert
        #register_links(['django_gpg:key_delete', 'django_gpg:key_public_list', 'django_gpg:key_query'], [public_keys, key_query], menu_name='sidebar')
        #register_links(Key, [key_delete])
        #register_links(KeyServerKey, [key_receive])
        menu_setup.bind_links(links=[link_key_setup])
