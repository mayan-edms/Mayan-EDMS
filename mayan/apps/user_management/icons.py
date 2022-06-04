from mayan.apps.appearance.classes import Icon

# App

icon_group = Icon(driver_name='fontawesome', symbol='users')
icon_user_setup = Icon(driver_name='fontawesome', symbol='user')

# Current user

icon_current_user_detail = Icon(driver_name='fontawesome', symbol='user')

# Group

icon_group_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='users',
    secondary_symbol='plus'
)
icon_group_detail = Icon(driver_name='fontawesome', symbol='users')
icon_group_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_group_list = Icon(driver_name='fontawesome', symbol='users')
icon_group_multiple_delete = Icon(driver_name='fontawesome', symbol='times')
icon_group_setup = Icon(driver_name='fontawesome', symbol='users')
icon_group_single_delete = Icon(driver_name='fontawesome', symbol='times')
icon_group_user_list = Icon(driver_name='fontawesome', symbol='user')

# User

icon_user_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='user',
    secondary_symbol='plus'
)
icon_user_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_user_group_list = icon_group
icon_user_list = Icon(driver_name='fontawesome', symbol='user')
icon_user_multiple_delete = Icon(driver_name='fontawesome', symbol='times')
icon_user_multiple_set_password = Icon(
    driver_name='fontawesome', symbol='key'
)
icon_user_set_options = Icon(driver_name='fontawesome', symbol='cog')
icon_user_single_delete = Icon(driver_name='fontawesome', symbol='times')
