from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation import Link

from .icons import icon_namespace_list
from .permissions import permission_settings_edit, permission_settings_view

link_namespace_list = Link(
    icon_class=icon_namespace_list, permissions=(permission_settings_view,),
    text=_('Settings'), view='settings:namespace_list'
)
link_namespace_detail = Link(
    args='resolved_object.name', permissions=(permission_settings_view,),
    text=_('Settings'), view='settings:namespace_detail',
)
# Duplicate the link to use a different name
link_namespace_root_list = Link(
    icon_class=icon_namespace_list, permissions=(permission_settings_view,),
    text=_('Namespaces'), view='settings:namespace_list'
)
link_setting_edit = Link(
    args='resolved_object.global_name', permissions=(permission_settings_edit,),
    text=_('Edit'), view='settings:setting_edit_view',
)
