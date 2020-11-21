from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Menu
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import icon_cabinet_list
from .permissions import permission_cabinet_create, permission_cabinet_view

menu_cabinets = Menu(
    condition=get_cascade_condition(
        app_label='cabinets', model_name='Cabinet',
        object_permission=permission_cabinet_view,
        view_permission=permission_cabinet_create,
    ), icon=icon_cabinet_list, label=_('Cabinets'), name='cabinets'
)
