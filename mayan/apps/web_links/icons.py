from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_type

icon_web_link = Icon(driver_name='fontawesome', symbol='external-link-alt')
icon_document_type_web_links = icon_web_link
icon_document_web_link_list = Icon(
    driver_name='fontawesome', symbol='external-link-alt'
)
icon_web_link_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='external-link-alt',
    secondary_symbol='plus'
)
icon_web_link_delete = Icon(driver_name='fontawesome', symbol='times')
icon_web_link_document_types = icon_document_type
icon_web_link_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_web_link_instance_view = Icon(
    driver_name='fontawesome', symbol='external-link-alt'
)
icon_web_link_setup = icon_web_link
icon_web_link_list = icon_web_link
