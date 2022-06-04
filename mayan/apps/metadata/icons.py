from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_type

icon_metadata = Icon(driver_name='fontawesome', symbol='database')

# Document metadata

icon_document_metadata_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='plus'
)
icon_document_metadata_edit = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='pen'
)
icon_document_metadata_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='minus'
)
icon_document_metadata_list = Icon(
    driver_name='fontawesome', symbol='database'
)
icon_document_multiple_metadata_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='plus'
)
icon_document_multiple_metadata_edit = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='pen'
)
icon_document_multiple_metadata_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='minus'
)

# Document type

icon_document_type_metadata_type_list = Icon(
    driver_name='fontawesome', symbol='database'
)

# Metadata type

icon_metadata_type_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='database',
    secondary_symbol='plus'
)
icon_metadata_type_single_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_metadata_type_multiple_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_metadata_type_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_metadata_type_list = Icon(driver_name='fontawesome', symbol='database')
icon_metadata_type_document_type_list = icon_document_type
