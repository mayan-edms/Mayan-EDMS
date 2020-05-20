from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig


class DashboardsApp(MayanAppConfig):
    app_namespace = 'dashboards'
    app_url = 'dashboards'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.dashboards'
    verbose_name = _('Dashboards')
