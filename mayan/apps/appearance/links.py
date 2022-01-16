from django.utils.translation import ugettext_lazy as _

from mayan.apps.authentication.link_conditions import condition_user_is_authenticated
from mayan.apps.navigation.classes import Link

from .icons import (
    icon_user_theme_settings_detail,
    icon_user_theme_settings_edit, icon_theme_create,
    icon_theme_delete, icon_theme_edit, icon_theme_list, icon_theme_setup
)
from .permissions import (
    permission_theme_create, permission_theme_delete, permission_theme_edit,
)

link_user_theme_settings_detail = Link(
    args='object.pk',
    icon=icon_user_theme_settings_detail,
    text=_('Theme settings'),
    view='appearance:user_theme_settings_detail'
)
link_user_theme_settings_edit = Link(
    args='object.pk',
    condition=condition_user_is_authenticated,
    icon=icon_user_theme_settings_edit,
    text=_('Edit theme settings'),
    view='appearance:user_theme_settings_edit'
)

link_theme_create = Link(
    icon=icon_theme_create, permissions=(permission_theme_create,),
    text=_('Create new theme'), view='appearance:theme_create'
)
link_theme_delete = Link(
    args='object.pk', icon=icon_theme_delete,
    permissions=(permission_theme_delete,), tags='dangerous',
    text=_('Delete'), view='appearance:theme_delete'
)
link_theme_edit = Link(
    args='object.pk', icon=icon_theme_edit,
    permissions=(permission_theme_edit,), text=_('Edit'),
    view='appearance:theme_edit'
)
link_theme_list = Link(
    icon=icon_theme_list, text=_('Themes'),
    view='appearance:theme_list'
)
link_theme_setup = Link(
    icon=icon_theme_setup, permissions=(permission_theme_create,),
    text=_('Themes'), view='appearance:theme_list'
)
