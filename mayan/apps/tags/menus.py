from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Menu

from .icons import icon_menu_tags

menu_tags = Menu(
    icon_class=icon_menu_tags, label=_('Tags'), name='tags menu'
)
