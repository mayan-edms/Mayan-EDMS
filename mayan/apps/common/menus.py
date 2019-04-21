from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation import Menu

from .icons import icon_menu_about, icon_menu_user

__all__ = (
    'menu_about', 'menu_facet', 'menu_object', 'menu_main', 'menu_multi_item',
    'menu_secondary', 'menu_setup', 'menu_sidebar', 'menu_tools', 'menu_user'
)

menu_about = Menu(
    icon_class=icon_menu_about, label=_('System'), name='about'
)
menu_facet = Menu(label=_('Facet'), name='facet')
menu_main = Menu(name='main')
menu_multi_item = Menu(name='multi item')
menu_object = Menu(label=_('Actions'), name='object')
menu_secondary = Menu(label=_('Secondary'), name='secondary')
menu_setup = Menu(name='setup')
menu_sidebar = Menu(name='sidebar')
menu_tools = Menu(name='tools')
menu_user = Menu(
    icon_class=icon_menu_user, name='user', label=_('User')
)
