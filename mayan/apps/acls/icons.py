from mayan.apps.appearance.classes import Icon
from mayan.apps.permissions.icons import icon_permission

icon_acl_delete = Icon(driver_name='fontawesome', symbol='times')
icon_acl_list = Icon(driver_name='fontawesome', symbol='lock')
icon_acl_new = Icon(
    driver_name='fontawesome-dual', primary_symbol='lock',
    secondary_symbol='plus'
)
icon_acl_permissions = icon_permission
