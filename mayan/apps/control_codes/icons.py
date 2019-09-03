from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_type

icon_control_code = Icon(driver_name='fontawesome', symbol='qrcode')
icon_control_code_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='qrcode',
    secondary_symbol='plus'
)
icon_control_code_delete = Icon(driver_name='fontawesome', symbol='times')
icon_control_code_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_control_code_list = Icon(driver_name='fontawesome', symbol='qrcode')
icon_control_code_preview = Icon(driver_name='fontawesome', symbol='print')
icon_control_sheet_code_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_control_sheet_code_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_control_sheet_code_list = Icon(
    driver_name='fontawesome', symbol='qrcode'
)
