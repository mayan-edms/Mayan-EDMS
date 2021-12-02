from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import menu_secondary, menu_tools, menu_object
from mayan.apps.navigation.classes import SourceColumn

from .classes import Dashboard
from .links import link_dashboard_detail, link_dashboard_list


class DashboardsApp(MayanAppConfig):
    app_namespace = 'dashboards'
    app_url = 'dashboards'
    has_rest_api = False
    has_static_media = True
    has_tests = True
    name = 'mayan.apps.dashboards'
    verbose_name = _('Dashboards')

    def ready(self):
        super().ready()

        SourceColumn(
            func=lambda context: len(context['object'].widgets),
            label=_('Widgets'), include_label=True,
            source=Dashboard
        )
        SourceColumn(
            attribute='label', label=_('Label'), is_identifier=True,
            source=Dashboard
        )

        menu_object.bind_links(
            links=(link_dashboard_detail,), sources=(Dashboard,)
        )

        menu_secondary.bind_links(
            links=(link_dashboard_list,), sources=(
                Dashboard, 'dashboards:dashboard_list',
            )
        )
        menu_tools.bind_links(links=(link_dashboard_list,))
