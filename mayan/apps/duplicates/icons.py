from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_list

icon_duplicate_backend_list = Icon(
    driver_name='fontawesome', symbol='clone'
)
icon_duplicated_document_list = icon_document_list
icon_duplicated_document_scan = Icon(
    driver_name='fontawesome-dual-classes', primary_class='fas fa-clone',
    secondary_class='far fa-eye'
)
