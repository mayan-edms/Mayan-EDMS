from __future__ import unicode_literals

from hkp import Key as KeyServerKey

from navigation.api import register_links
from project_setup.api import register_setup

from .api import Key
from .links import (
    key_delete, key_query, key_receive, key_setup, public_keys
)

register_links(['django_gpg:key_delete', 'django_gpg:key_public_list', 'django_gpg:key_query'], [public_keys, key_query], menu_name='sidebar')
register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])
register_setup(key_setup)
