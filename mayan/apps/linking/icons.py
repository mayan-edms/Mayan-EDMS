from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_type

icon_smart_link = Icon(driver_name='fontawesome', symbol='link')

icon_document_type_smart_links = icon_smart_link

icon_smart_link_condition = Icon(driver_name='fontawesome', symbol='code')
icon_smart_link_condition_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='code',
    secondary_symbol='plus'
)
icon_smart_link_condition_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_smart_link_condition_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_smart_link_condition_list = icon_smart_link_condition
icon_smart_link_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='link',
    secondary_symbol='plus'
)
icon_smart_link_delete = Icon(driver_name='fontawesome', symbol='times')
icon_smart_link_document_types = icon_document_type
icon_smart_link_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_smart_link_instances_for_document = Icon(
    driver_name='fontawesome', symbol='link'
)
icon_smart_link_setup = icon_smart_link
icon_smart_link_list = icon_smart_link
