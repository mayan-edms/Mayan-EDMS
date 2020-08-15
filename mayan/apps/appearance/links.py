from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_current_user_theme_settings_details,
    icon_current_user_theme_settings_edit
)
from .permissions import (
    permission_theme_create, permission_theme_delete, permission_theme_edit,
)

link_current_user_theme_settings_details = Link(
    icon_class=icon_current_user_theme_settings_details,
    text=_('Theme settings'),
    view='appearance:current_user_theme_settings_details'
)
link_current_user_theme_settings_edit = Link(
    icon_class=icon_current_user_theme_settings_edit,
    text=_('Edit theme settings'),
    view='appearance:current_user_theme_settings_edit'
)

link_theme_create = Link(
    icon_class_path='mayan.apps.appearance.icons.icon_theme_create',
    permissions=(permission_theme_create,),
    text=_('Create new theme'), view='appearance:theme_create'
)
link_theme_delete = Link(
    args='object.pk',
    icon_class_path='mayan.apps.appearance.icons.icon_theme_delete',
    permissions=(permission_theme_delete,),
    tags='dangerous', text=_('Delete'), view='appearance:theme_delete',
)
link_theme_edit = Link(
    args='object.pk',
    icon_class_path='mayan.apps.appearance.icons.icon_theme_edit',
    permissions=(permission_theme_edit,),
    text=_('Edit'), view='appearance:theme_edit',
)
link_theme_list = Link(
    icon_class_path='mayan.apps.appearance.icons.icon_theme_list',
    text=_('Themes'), view='appearance:theme_list'
)
link_theme_setup = Link(
    icon_class_path='mayan.apps.appearance.icons.icon_theme_setup',
    permissions=(permission_theme_create,), text=_('Themes'),
    view='appearance:theme_list'
)
