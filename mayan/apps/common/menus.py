from __future__ import unicode_literals

from navigation import Menu

__all__ = (
    'menu_facet', 'menu_front_page', 'menu_object', 'menu_main',
    'menu_multi_item', 'menu_secondary', 'menu_setup', 'menu_sidebar',
    'menu_tools'
)

menu_facet = Menu(name='object facet')
menu_front_page = Menu(name='front page menu')
menu_object = Menu(name='object menu')
menu_main = Menu(name='main menu')
menu_multi_item = Menu(name='multi item menu')
menu_secondary = Menu(name='secondary menu')
menu_setup = Menu(name='setup menu')
menu_sidebar = Menu(name='sidebar menu')
menu_tools = Menu(name='tools menu')
