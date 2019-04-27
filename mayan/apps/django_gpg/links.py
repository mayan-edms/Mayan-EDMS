from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_key_setup, icon_key_upload, icon_keyserver_search
from .permissions import (
    permission_key_delete, permission_key_download, permission_key_receive,
    permission_key_view, permission_key_upload, permission_keyserver_query
)

link_key_delete = Link(
    args=('resolved_object.pk',), permissions=(permission_key_delete,),
    tags='dangerous', text=_('Delete'), view='django_gpg:key_delete',
)
link_key_detail = Link(
    args=('resolved_object.pk',), permissions=(permission_key_view,),
    text=_('Details'), view='django_gpg:key_detail',
)
link_key_download = Link(
    args=('resolved_object.pk',), permissions=(permission_key_download,),
    text=_('Download'), view='django_gpg:key_download',
)
link_key_query = Link(
    icon_class=icon_keyserver_search,
    permissions=(permission_keyserver_query,), text=_('Query keyservers'),
    view='django_gpg:key_query'
)
link_key_receive = Link(
    args='object.key_id', keep_query=True,
    permissions=(permission_key_receive,), text=_('Import'),
    view='django_gpg:key_receive',
)
link_key_setup = Link(
    icon_class=icon_key_setup, permissions=(permission_key_view,),
    text=_('Key management'), view='django_gpg:key_public_list'
)
link_key_upload = Link(
    icon_class=icon_key_upload, permissions=(permission_key_upload,),
    text=_('Upload key'), view='django_gpg:key_upload'
)
link_private_keys = Link(
    permissions=(permission_key_view,), text=_('Private keys'),
    view='django_gpg:key_private_list'
)
link_public_keys = Link(
    permissions=(permission_key_view,), text=_('Public keys'),
    view='django_gpg:key_public_list'
)
