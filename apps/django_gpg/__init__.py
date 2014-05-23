from __future__ import absolute_import

from hkp import Key as KeyServerKey

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links
from project_setup.api import register_setup

from .api import Key
from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)

# Setup views
private_keys = {'text': _(u'private keys'), 'view': 'key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _(u'public keys'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _(u'delete'), 'view': 'key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _(u'query keyservers'), 'view': 'key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _(u'import'), 'view': 'key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
key_setup = {'text': _(u'key management'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW], 'children_view_regex': [r'^key_']}

# register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
register_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])

register_setup(key_setup)
