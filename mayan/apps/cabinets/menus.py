from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Menu, get_cascade_condition

from .icons import icon_cabinet_list
from .permissions import permission_cabinet_create, permission_cabinet_view

menu_cabinets = Menu(
    condition=get_cascade_condition(
        app_label='cabinets', model_name='Cabinet',
        object_permission=permission_cabinet_view,
        view_permission=permission_cabinet_create,
    ), icon_class=icon_cabinet_list, label=_('Cabinets'), name='cabinets menu'
)
