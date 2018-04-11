from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Menu

from .icons import icon_cabinet_list

menu_cabinets = Menu(
    icon_class=icon_cabinet_list, label=_('Cabinets'), name='cabinets menu'
)
