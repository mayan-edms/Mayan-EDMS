from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, Link
from project_setup.api import register_setup
from hkp import Key as KeyServerKey

from .api import Key
from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)

# Setup views
private_keys = Link(text=_(u'private keys'), view='key_private_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW])
public_keys = Link(text=_(u'public keys'), view='key_public_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW])
key_delete = Link(text=_(u'delete'), view='key_delete', args=['object.fingerprint', 'object.type'], sprite='key_delete', permissions=[PERMISSION_KEY_DELETE])
key_query = Link(text=_(u'query keyservers'), view='key_query', sprite='zoom', permissions=[PERMISSION_KEYSERVER_QUERY])
key_receive = Link(text=_(u'import'), view='key_receive', args='object.keyid', sprite='key_add', keep_query=True, permissions=[PERMISSION_KEY_RECEIVE])
key_setup = Link(text=_(u'key management'), view='key_public_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW], children_view_regex=[r'^key_'])

#bind_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
bind_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

bind_links([Key], [key_delete])
bind_links([KeyServerKey], [key_receive])

register_setup(key_setup)
