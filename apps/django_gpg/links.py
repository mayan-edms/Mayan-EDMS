from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (icon_private_keys, icon_public_keys, icon_key_delete,
    icon_key_query, icon_key_receive, icon_key_setup)
from .permissions import (PERMISSION_KEY_VIEW, PERMISSION_KEY_DELETE,
    PERMISSION_KEYSERVER_QUERY, PERMISSION_KEY_RECEIVE)

private_keys = Link(text=_(u'private keys'), view='key_private_list', args='object.pk', icon=icon_private_keys, permissions=[PERMISSION_KEY_VIEW])
public_keys = Link(text=_(u'public keys'), view='key_public_list', args='object.pk', icon=icon_private_keys, permissions=[PERMISSION_KEY_VIEW])
key_delete = Link(text=_(u'delete'), view='key_delete', args=['object.fingerprint', 'object.type'], icon=icon_key_delete, permissions=[PERMISSION_KEY_DELETE])
key_query = Link(text=_(u'query keyservers'), view='key_query', icon=icon_key_query, permissions=[PERMISSION_KEYSERVER_QUERY])
key_receive = Link(text=_(u'import'), view='key_receive', args='object.keyid', icon=icon_key_receive, keep_query=True, permissions=[PERMISSION_KEY_RECEIVE])
key_setup = Link(text=_(u'key management'), view='key_public_list', args='object.pk', icon=icon_key_setup, permissions=[PERMISSION_KEY_VIEW], children_view_regex=[r'^key_'])
