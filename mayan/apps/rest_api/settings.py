from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import DEFAULT_REST_API_DISABLE_LINKS

namespace = SettingNamespace(
    label=_('REST API'), name='rest_api', version='0001'
)

setting_disable_links = namespace.add_setting(
    default=DEFAULT_REST_API_DISABLE_LINKS,
    global_name='REST_API_DISABLE_LINKS', help_text=_(
        'Disable the REST API links in the tools menu.'
    )
)
