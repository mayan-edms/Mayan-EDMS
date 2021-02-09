from mayan.apps.appearance.classes import Icon

icon_add_all = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-circle'},
        {'class': 'fas fa-plus', 'transform': 'shrink-6'}
    ]
)
icon_assign_remove_add = Icon(driver_name='fontawesome', symbol='plus')
icon_assign_remove_remove = Icon(driver_name='fontawesome', symbol='minus')
icon_confirm_form_submit = Icon(driver_name='fontawesome', symbol='check')
icon_confirm_form_cancel = Icon(driver_name='fontawesome', symbol='times')
icon_fail = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_list_mode_list = Icon(
    driver_name='fontawesome', symbol='list'
)
icon_list_mode_items = Icon(
    driver_name='fontawesome', symbol='th-large'
)
icon_ok = Icon(
    driver_name='fontawesome', symbol='check'
)
icon_remove_all = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-circle'},
        {'class': 'fas fa-minus', 'transform': 'shrink-6'}
    ]
)
icon_sort_down = Icon(driver_name='fontawesome', symbol='sort-down')
icon_sort_up = Icon(driver_name='fontawesome', symbol='sort-up')
