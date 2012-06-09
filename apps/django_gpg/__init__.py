from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, Link
from project_setup.api import register_setup
from hkp import Key as KeyServerKey

from .api import Key
from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)
from .links import (private_keys, public_keys, key_delete, key_query,
    key_receive, key_setup)

#bind_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
bind_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

bind_links([Key], [key_delete])
bind_links([KeyServerKey], [key_receive])

register_setup(key_setup)
