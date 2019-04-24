from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_group_roles = Icon(driver_name='fontawesome', symbol='user-secret')
icon_permission = Icon(driver_name='fontawesome', symbol='thumbs-up')
icon_role_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='user-secret',
    secondary_symbol='plus'
)
icon_role_delete = Icon(driver_name='fontawesome', symbol='times')
icon_role_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_role_groups = Icon(driver_name='fontawesome', symbol='users')
icon_role_list = Icon(driver_name='fontawesome', symbol='user-secret')
icon_role_permissions = Icon(driver_name='fontawesome', symbol='thumbs-up')
