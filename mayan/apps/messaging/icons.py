from mayan.apps.appearance.classes import Icon

icon_message_create = icon_tag_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='comment-alt',
    secondary_symbol='plus'
)
icon_message_delete = Icon(driver_name='fontawesome', symbol='times')
icon_message_detail = Icon(driver_name='fontawesome', symbol='comment-alt')
icon_message_list = Icon(driver_name='fontawesome', symbol='comment-alt')
icon_message_mark_read = Icon(driver_name='fontawesome', symbol='eye')
icon_message_mark_unread = Icon(
    driver_name='fontawesome', symbol='eye-slash'
)
icon_message_mark_read_all = Icon(driver_name='fontawesome', symbol='eye')
