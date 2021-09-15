from mayan.apps.appearance.classes import Icon

# Document file

icon_document_file_content = Icon(driver_name='fontawesome', symbol='font')
icon_document_file_content_delete_single = Icon(
    driver_name='fontawesome-dual', primary_symbol='font',
    secondary_symbol='times'
)
icon_document_file_content_delete_multiple = icon_document_file_content_delete_single
icon_document_file_content_download = Icon(
    driver_name='fontawesome-dual', primary_symbol='font',
    secondary_symbol='arrow-down'
)
icon_document_file_page_content = icon_document_file_content
icon_document_file_parsing_errors_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='font',
    secondary_symbol='exclamation'
)
icon_document_file_submit_multiple = Icon(
    driver_name='fontawesome-dual', primary_symbol='font',
    secondary_symbol='arrow-right'
)
icon_document_file_submit = icon_document_file_submit_multiple
icon_document_type_parsing_settings = Icon(
    driver_name='fontawesome', symbol='font'
)

# Document type

icon_document_type_submit = icon_document_file_submit_multiple

# Errors

icon_error_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='font',
    secondary_symbol='exclamation'
)
