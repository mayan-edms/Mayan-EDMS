from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_api, icon_api_documentation, icon_api_documentation_redoc
)


link_api = Link(
    icon_class=icon_api, tags='new_window', text=_('REST API'),
    view='rest_api:api_root'
)
link_api_documentation = Link(
    icon_class=icon_api_documentation, tags='new_window',
    text=_('API Documentation (Swagger)'), view='rest_api:schema-swagger-ui'
)

link_api_documentation_redoc = Link(
    icon_class=icon_api_documentation_redoc, tags='new_window',
    text=_('API Documentation (ReDoc)'), view='rest_api:schema-redoc'
)
