from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_message_create = icon_tag_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='bullhorn',
    secondary_symbol='plus'
)
icon_message_delete = Icon(driver_name='fontawesome', symbol='times')
icon_message_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_message_list = Icon(driver_name='fontawesome', symbol='bullhorn')
