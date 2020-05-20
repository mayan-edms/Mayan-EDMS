from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_api, icon_api_documentation, icon_api_documentation_redoc
)
from .settings import setting_disable_links


def api_links_enabled(context):
    return not setting_disable_links.value


link_api = Link(
    condition=api_links_enabled, icon_class=icon_api, tags='new_window',
    text=_('REST API'), view='rest_api:api_root'
)
link_api_documentation = Link(
    condition=api_links_enabled, icon_class=icon_api_documentation,
    tags='new_window', text=_('API Documentation (Swagger)'),
    view='rest_api:schema-swagger-ui'
)

link_api_documentation_redoc = Link(
    condition=api_links_enabled, icon_class=icon_api_documentation_redoc,
    tags='new_window', text=_('API Documentation (ReDoc)'),
    view='rest_api:schema-redoc'
)
