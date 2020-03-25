from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu

from .icons import icon_menu_about, icon_menu_user

menu_about = Menu(
    icon_class=icon_menu_about, label=_('System'), name='about'
)
menu_facet = Menu(label=_('Facet'), name='facet')
menu_list_facet = Menu(label=_('Facet'), name='list facet')
menu_main = Menu(name='main')
menu_multi_item = Menu(name='multi item')
menu_object = Menu(label=_('Actions'), name='object')
menu_secondary = Menu(label=_('Secondary'), name='secondary')
menu_setup = Menu(name='setup')
menu_tools = Menu(name='tools')
menu_topbar = Menu(name='topbar')
menu_user = Menu(
    icon_class=icon_menu_user, name='user', label=_('User')
)
