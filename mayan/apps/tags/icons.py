from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_list

icon_menu_tags = Icon(driver_name='fontawesome', symbol='tags')

# Documents

icon_document_multiple_tag_multiple_attach = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-right'
)
icon_document_multiple_tag_multiple_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-left'
)
icon_document_tag_multiple_attach = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-right'
)
icon_document_tag_multiple_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-left'
)
icon_document_tag_list = Icon(driver_name='fontawesome', symbol='tags')

# Tags

icon_tag_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='plus'
)
icon_tag_single_delete = Icon(driver_name='fontawesome', symbol='times')
icon_tag_multiple_delete = Icon(driver_name='fontawesome', symbol='times')
icon_tag_document_list = icon_document_list
icon_tag_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_tag_list = Icon(driver_name='fontawesome', symbol='tag')
