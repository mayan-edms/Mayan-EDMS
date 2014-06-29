from __future__ import absolute_import

from hkp import Key as KeyServerKey

from navigation.api import register_links
from project_setup.api import register_setup

from .api import Key
from .links import (public_keys, key_delete, key_query, key_receive,
    key_setup)

# register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
register_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])

register_setup(key_setup)
