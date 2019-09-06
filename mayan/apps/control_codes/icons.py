from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon

icon_control_sheet = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-file'},
        {'class': 'fas fa-barcode', 'transform': 'shrink-6'},
    ], shadow_class='far fa-file',
)
icon_control_sheet_create = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-file ', 'transform': 'grow-4'},
        {'class': 'fas fa-barcode', 'transform': 'shrink-6'},
        {'class': 'far fa-circle', 'transform': 'down-5 right-10'},
        {'class': 'fas fa-plus', 'transform': 'shrink-4 down-5 right-10'},
    ],
)
icon_control_sheet_delete = Icon(driver_name='fontawesome', symbol='times')
icon_control_sheet_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_control_sheet_list = icon_control_sheet
icon_control_sheet_preview = Icon(driver_name='fontawesome', symbol='eye')
icon_control_sheet_print = Icon(driver_name='fontawesome', symbol='print')

icon_control_sheet_code = Icon(driver_name='fontawesome', symbol='barcode')
icon_control_sheet_code_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_control_sheet_code_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_control_sheet_code_list = Icon(
    driver_name='fontawesome', symbol='barcode'
)
icon_control_sheet_code_select = Icon(
    driver_name='fontawesome-dual', primary_symbol='barcode',
    secondary_symbol='plus'
)
