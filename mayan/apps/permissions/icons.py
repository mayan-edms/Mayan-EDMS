from mayan.apps.appearance.classes import Icon

# App

icon_permission = Icon(driver_name='fontawesome', symbol='thumbs-up')

# Group

icon_group_role_list = Icon(driver_name='fontawesome', symbol='user-secret')

# Permission

icon_permission_detail = Icon(driver_name='fontawesome', symbol='thumbs-up')

# Role

icon_role_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='user-secret',
    secondary_symbol='plus'
)
icon_role_single_delete = Icon(driver_name='fontawesome', symbol='times')
icon_role_multiple_delete = icon_role_single_delete
icon_role_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_role_group_list = Icon(driver_name='fontawesome', symbol='users')
icon_role_list = Icon(driver_name='fontawesome', symbol='user-secret')
icon_role_permission_list = Icon(
    driver_name='fontawesome', symbol='thumbs-up'
)
