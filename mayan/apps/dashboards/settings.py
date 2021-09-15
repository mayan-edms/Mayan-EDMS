from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import DEFAULT_DASHBOARDS_DEFAULT_DASHBOARD_NAME

namespace = SettingNamespace(label=_('Dashboards'), name='dashboards')

setting_default_dashboard_name = namespace.add_setting(
    default=DEFAULT_DASHBOARDS_DEFAULT_DASHBOARD_NAME,
    global_name='DASHBOARDS_DEFAULT_DASHBOARD_NAME',
    help_text=_(
        'In list mode, show the "list facet" menu options as a dropdown '
        'menu instead of individual buttons.'
    )
)
