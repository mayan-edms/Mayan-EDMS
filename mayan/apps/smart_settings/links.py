from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_namespace_list
from .permissions import permission_settings_view

link_namespace_list = Link(
    icon_class=icon_namespace_list, permissions=(permission_settings_view,),
    text=_('Settings'), view='settings:namespace_list'
)
link_namespace_detail = Link(
    args='resolved_object.name', permissions=(permission_settings_view,),
    text=_('Settings'), view='settings:namespace_detail',
)
