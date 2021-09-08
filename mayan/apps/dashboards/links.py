from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import icon_dashboard_detail, icon_dashboard_list


link_dashboard_list = Link(
    icon=icon_dashboard_list, text=_('Dashboards'), view='dashboards:dashboard_list'
)

link_dashboard_detail = Link(
    args='object.name', icon=icon_dashboard_detail,
    text=_('Details'), view='dashboards:dashboard_detail'
)
