from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_acl_delete = Icon(driver_name='fontawesome', symbol='times')
icon_acl_list = Icon(driver_name='fontawesome', symbol='lock')
icon_acl_new = Icon(
    driver_name='fontawesome-dual', primary_symbol='lock',
    secondary_symbol='plus'
)
