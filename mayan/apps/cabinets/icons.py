from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_cabinet = Icon(driver_name='fontawesome', symbol='columns')
icon_cabinet_add = Icon(driver_name='fontawesome', symbol='plus')
icon_cabinet_child_add = Icon(driver_name='fontawesome', symbol='plus')
icon_cabinet_create = Icon(driver_name='fontawesome', symbol='plus')

icon_cabinet_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='columns',
    secondary_symbol='plus'
)

icon_cabinet_delete = Icon(driver_name='fontawesome', symbol='times')
icon_cabinet_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_cabinet_list = Icon(driver_name='fontawesome', symbol='columns')
icon_cabinet_view = Icon(driver_name='fontawesome', symbol='columns')

icon_document_cabinet_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='columns',
    secondary_symbol='arrow-right'
)
icon_document_cabinet_list = icon_cabinet_list
icon_document_cabinet_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='columns',
    secondary_symbol='minus'
)
icon_document_multiple_cabinet_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='columns',
    secondary_symbol='arrow-right'
)
icon_document_multiple_cabinet_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='columns',
    secondary_symbol='minus'
)
