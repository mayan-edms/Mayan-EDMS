from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_ORGANIZATIONS_INSTALLATION_URL,
    DEFAULT_ORGANIZATIONS_URL_BASE_PATH
)

namespace = SettingNamespace(label=_('Organizations'), name='organizations')

setting_organization_installation_url = namespace.add_setting(
    default=DEFAULT_ORGANIZATIONS_INSTALLATION_URL,
    global_name='ORGANIZATIONS_INSTALLATION_URL',
    help_text=_(
        'Fully qualified URL including scheme and port number if using a '
        'custom one. Example: https://www.example.com:8080'
    )
)
setting_organization_url_base_path = namespace.add_setting(
    default=DEFAULT_ORGANIZATIONS_URL_BASE_PATH,
    global_name='ORGANIZATIONS_URL_BASE_PATH',
    help_text=_(
        'Base URL path to use for all views. Used when hosting using a path '
        'that is not the root path of the web server.'
    )
)
