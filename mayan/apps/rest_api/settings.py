from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import SettingNamespace

from .literals import (
    DEFAULT_REST_API_DISABLE_LINKS, DEFAULT_REST_API_MAXIMUM_PAGE_SIZE,
    DEFAULT_REST_API_PAGE_SIZE
)

namespace = SettingNamespace(
    label=_('REST API'), name='rest_api', version='0001'
)

setting_disable_links = namespace.add_setting(
    default=DEFAULT_REST_API_DISABLE_LINKS,
    global_name='REST_API_DISABLE_LINKS', help_text=_(
        'Disable the REST API links in the tools menu.'
    )
)
setting_maximum_page_size = namespace.add_setting(
    default=DEFAULT_REST_API_MAXIMUM_PAGE_SIZE,
    global_name='REST_API_MAXIMUM_PAGE_SIZE', help_text=_(
        'The maximum page size that can be requested.'
    )
)
setting_page_size = namespace.add_setting(
    default=DEFAULT_REST_API_PAGE_SIZE,
    global_name='REST_API_PAGE_SIZE', help_text=_(
        'The default page size if none is specified.'
    )
)
