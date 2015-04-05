from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    PERMISSION_KEY_DELETE, PERMISSION_KEY_RECEIVE, PERMISSION_KEY_VIEW,
    PERMISSION_KEYSERVER_QUERY
)

link_private_keys = Link(icon='fa fa-key', permissions=[PERMISSION_KEY_VIEW], text=_('Private keys'), view='django_gpg:key_private_list')
link_public_keys = Link(icon='fa fa-key', permissions=[PERMISSION_KEY_VIEW], text=_('Public keys'), view='django_gpg:key_public_list')
link_key_delete = Link(permissions=[PERMISSION_KEY_DELETE], text=_('Delete'), view='django_gpg:key_delete', args=['object.fingerprint', 'object.type'])
link_key_query = Link(text=_('Query keyservers'), view='django_gpg:key_query', permissions=[PERMISSION_KEYSERVER_QUERY])
link_key_receive = Link(keep_query=True, permissions=[PERMISSION_KEY_RECEIVE], text=_('Import'), view='django_gpg:key_receive', args='object.keyid')
link_key_setup = Link(icon='fa fa-key', permissions=[PERMISSION_KEY_VIEW], text=_('Key management'), view='django_gpg:key_public_list')
