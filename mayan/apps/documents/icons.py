from mayan.apps.appearance.classes import Icon
from mayan.apps.converter.icons import icon_transformations

icon_document_type = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'fas fa-circle', 'transform': 'shrink-12 up-2'},
        {'class': 'fas fa-cog', 'transform': 'shrink-6 up-2', 'mask': 'fas fa-torah'}
    ]
)

icon_menu_documents = Icon(driver_name='fontawesome', symbol='book')

icon_dashboard_document_types = icon_document_type
icon_dashboard_documents_in_trash = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)
icon_dashboard_pages_per_month = Icon(
    driver_name='fontawesome', symbol='copy'
)
icon_dashboard_new_documents_this_month = Icon(
    driver_name='fontawesome', symbol='calendar'
)
icon_dashboard_total_document = Icon(
    driver_name='fontawesome', symbol='book'
)
icon_document_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_document = Icon(driver_name='fontawesome', symbol='book')
icon_document_list = icon_document
icon_document_file_page_count_update = Icon(
    driver_name='fontawesome', symbol='copy'
)
icon_document_preview = Icon(driver_name='fontawesome', symbol='eye')
icon_document_properties = Icon(driver_name='fontawesome', symbol='info')
icon_document_trash_send = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)


icon_document_type_change = icon_document_type

icon_document_image_loading = Icon(
    driver_name='fontawesomecss', css_classes='far fa-clock fa-2x'
)
icon_document_list = Icon(driver_name='fontawesome', symbol='book')
icon_document_list_deleted = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)
icon_document_recently_accessed_list = Icon(
    driver_name='fontawesome', symbol='clock'
)
icon_document_return = Icon(
    driver_name='fontawesome-dual', primary_symbol='book',
    secondary_symbol='chevron-left'
)

# Favorites

icon_favorite_document_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='star',
    secondary_symbol='plus'
)
icon_favorite_document_list = Icon(driver_name='fontawesome', symbol='star')
icon_favorite_document_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='star',
    secondary_symbol='minus'
)

# Document files

icon_document_file_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_document_file_download_quick = Icon(
    driver_name='fontawesome', symbol='download'
)
icon_document_file_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_document_file_list = Icon(
    driver_name='fontawesome', symbol='hdd'
)
icon_document_file_preview = Icon(
    driver_name='fontawesome', symbol='eye'
)
icon_document_file_print = Icon(
    driver_name='fontawesome', symbol='print'
)
icon_document_file_properties = Icon(
    driver_name='fontawesome', symbol='info'
)
icon_document_file_return_to_document = icon_document_return
icon_document_file_return_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='hdd',
    secondary_symbol='chevron-left'
)
icon_document_file_transformations_clear = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='times'
)
icon_document_file_transformations_clone = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='arrow-right'
)

# Document file pages

icon_document_file_page_list = Icon(driver_name='fontawesome', symbol='copy')
icon_document_file_page_navigation_first = Icon(
    driver_name='fontawesome', symbol='step-backward'
)
icon_document_file_page_navigation_last = Icon(
    driver_name='fontawesome', symbol='step-forward'
)
icon_document_file_page_navigation_next = Icon(
    driver_name='fontawesome', symbol='arrow-right'
)
icon_document_file_page_navigation_previous = Icon(
    driver_name='fontawesome', symbol='arrow-left'
)
icon_document_file_page_return_to_document = icon_document_return
icon_document_file_page_return_to_document_file = Icon(
    driver_name='fontawesome-dual', primary_symbol='hdd',
    secondary_symbol='chevron-left'
)
icon_document_file_page_return_to_document_file_page_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='copy',
    secondary_symbol='chevron-left'
)
icon_document_file_page_rotate_left = Icon(
    driver_name='fontawesome', symbol='undo'
)
icon_document_file_page_rotate_right = Icon(
    driver_name='fontawesome', symbol='redo'
)
icon_document_file_page_view = Icon(
    driver_name='fontawesome', symbol='image'
)
icon_document_file_page_view_reset = Icon(
    driver_name='fontawesome', symbol='sync'
)
icon_document_file_page_zoom_in = Icon(
    driver_name='fontawesome', symbol='search-plus'
)
icon_document_file_page_zoom_out = Icon(
    driver_name='fontawesome', symbol='search-minus'
)

# Document types

icon_document_type_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='book',
    secondary_symbol='plus'
)
icon_document_type_delete = Icon(driver_name='fontawesome', symbol='times')
icon_document_type_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_document_type_setup = icon_document_type


icon_document_type_list = icon_document_type

icon_document_type_filename = Icon(
    driver_name='fontawesome', symbol='keyboard'
)
icon_document_type_filename_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='keyboard',
    secondary_symbol='plus'
)
icon_document_type_filename_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_document_type_filename_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_document_type_filename_list = Icon(
    driver_name='fontawesome', symbol='keyboard'
)

icon_document_type_filename_generator = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'far fa-file'},
        {'class': 'fas fa-cog', 'transform': 'shrink-8 down-2'}
    ]
)

icon_document_type_policies = Icon(driver_name='fontawesome', symbol='times')
icon_document_type_setup = icon_document_type

# Document version

icon_document_version_active = Icon(
    driver_name='fontawesome', symbol='check'
)
icon_document_version_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='code-branch',
    secondary_symbol='plus'
)
icon_document_version_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_document_version_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_document_version_export = Icon(
    driver_name='fontawesome', symbol='file-export'
)
icon_document_version_list = Icon(
    driver_name='fontawesome', symbol='code-branch'
)
icon_document_version_return_document = icon_document_return
icon_document_version_return_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='code-branch',
    secondary_symbol='chevron-left'
)
icon_document_version_preview = Icon(
    driver_name='fontawesome', symbol='eye'
)
icon_document_version_print = Icon(
    driver_name='fontawesome', symbol='print'
)
icon_document_version_transformations_clear = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='times'
)
icon_document_version_transformations_clone = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='arrow-right'
)

# Document version pages

icon_document_version_page_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_document_version_page_return_to_document = icon_document_return
icon_document_version_page_return_to_document_version = Icon(
    driver_name='fontawesome-dual', primary_symbol='code-branch',
    secondary_symbol='chevron-left'
)
icon_document_version_page_return_to_document_version_page_list = Icon(
    driver_name='fontawesome-dual', primary_symbol='copy',
    secondary_symbol='chevron-left'
)
icon_document_version_page_list = Icon(driver_name='fontawesome', symbol='copy')
icon_document_version_page_list_remap = Icon(
    driver_name='fontawesome', symbol='project-diagram'
)
icon_document_version_page_list_reset = Icon(
    driver_name='fontawesome', symbol='copy'
)
icon_document_version_page_navigation_first = Icon(
    driver_name='fontawesome', symbol='step-backward'
)
icon_document_version_page_navigation_last = Icon(
    driver_name='fontawesome', symbol='step-forward'
)
icon_document_version_page_navigation_next = Icon(
    driver_name='fontawesome', symbol='arrow-right'
)
icon_document_version_page_navigation_previous = Icon(
    driver_name='fontawesome', symbol='arrow-left'
)
icon_document_version_page_rotate_left = Icon(
    driver_name='fontawesome', symbol='undo'
)
icon_document_version_page_rotate_right = Icon(
    driver_name='fontawesome', symbol='redo'
)
icon_document_version_page_view = Icon(
    driver_name='fontawesome', symbol='image'
)
icon_document_version_page_view_reset = Icon(
    driver_name='fontawesome', symbol='sync'
)
icon_document_version_page_zoom_in = Icon(
    driver_name='fontawesome', symbol='search-plus'
)
icon_document_version_page_zoom_out = Icon(
    driver_name='fontawesome', symbol='search-minus'
)

# Recently created

icon_document_recently_created_list = Icon(
    driver_name='fontawesome', symbol='asterisk'
)

# Trashed documents

icon_trash_can_empty = Icon(
    driver_name='fontawesome-dual-classes', primary_class='fas fa-trash-alt',
    secondary_class='fas fa-minus'
)
icon_trashed_document_delete = Icon(
    driver_name='fontawesome', symbol='times'
)
icon_trashed_document_list = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)
icon_trashed_document_multiple_delete = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)
icon_trashed_document_multiple_restore = Icon(
    driver_name='fontawesome', symbol='recycle'
)
icon_trashed_document_restore = Icon(
    driver_name='fontawesome', symbol='recycle'
)
