from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)

private_keys = Link(text=_(u'private keys'), view='key_private_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW])
public_keys = Link(text=_(u'public keys'), view='key_public_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW])
key_delete = Link(text=_(u'delete'), view='key_delete', args=['object.fingerprint', 'object.type'], sprite='key_delete', permissions=[PERMISSION_KEY_DELETE])
key_query = Link(text=_(u'query keyservers'), view='key_query', sprite='zoom', permissions=[PERMISSION_KEYSERVER_QUERY])
key_receive = Link(text=_(u'import'), view='key_receive', args='object.keyid', sprite='key_add', keep_query=True, permissions=[PERMISSION_KEY_RECEIVE])
key_setup = Link(text=_(u'key management'), view='key_public_list', args='object.pk', sprite='key', icon='key.png', permissions=[PERMISSION_KEY_VIEW], children_view_regex=[r'^key_'])
