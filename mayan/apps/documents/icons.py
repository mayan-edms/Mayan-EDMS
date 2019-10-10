from __future__ import absolute_import, unicode_literals

from mayan.apps.appearance.classes import Icon
from mayan.apps.converter.icons import icon_transformations

icon_document_type = Icon(
    driver_name='fontawesome-layers', data=[
        {'class': 'fas fa-circle', 'transform': 'shrink-12 up-2'},
        {'class': 'fas fa-cog', 'transform': 'shrink-6 up-2', 'mask': 'fas fa-torah'}
    ], shadow_class='fas fa-torah'
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
icon_document_quick_download = Icon(
    driver_name='fontawesome', symbol='download'
)
icon_document_download = Icon(
    driver_name='fontawesome', symbol='download'
)
icon_document_edit = Icon(
    driver_name='fontawesome', symbol='pencil-alt'
)
icon_document = Icon(driver_name='fontawesome', symbol='book')
icon_document_list = icon_document
icon_document_pages_reset = Icon(
    driver_name='fontawesome', symbol='copy'
)
icon_document_version_page_count_update = Icon(
    driver_name='fontawesome', symbol='copy'
)
icon_document_preview = Icon(driver_name='fontawesome', symbol='eye')
icon_document_print = Icon(
    driver_name='fontawesome', symbol='print'
)
icon_document_properties = Icon(driver_name='fontawesome', symbol='info')
icon_document_trash_send = Icon(
    driver_name='fontawesome', symbol='trash-alt'
)

icon_document_transformations_clear = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='times'
)
icon_document_transformations_clone = Icon(
    driver_name='fontawesome-dual',
    primary_symbol=icon_transformations.kwargs['symbol'],
    secondary_symbol='arrow-right'
)

icon_document_type_change = icon_document_type
icon_document_type_create = Icon(driver_name='fontawesome', symbol='plus')
icon_document_type_delete = Icon(driver_name='fontawesome', symbol='times')
icon_document_type_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_document_type_setup = icon_document_type

icon_document_type_filename = Icon(
    driver_name='fontawesome', symbol='keyboard'
)
icon_document_type_filename_create = Icon(
    driver_name='fontawesome', symbol='plus'
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

icon_document_type_list = icon_document_type

icon_favorite_document_add = Icon(
    driver_name='fontawesome-dual', primary_symbol='star',
    secondary_symbol='plus'
)
icon_document_image_loading = Icon(
    driver_name='fontawesomecss', css_classes='far fa-clock fa-2x'
)
icon_document_list = Icon(driver_name='fontawesome', symbol='book')
icon_document_list_deleted = Icon(driver_name='fontawesome', symbol='trash')
icon_document_list_recent_access = Icon(
    driver_name='fontawesome', symbol='clock'
)

icon_favorite_document_list = Icon(driver_name='fontawesome', symbol='star')
icon_favorite_document_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='star',
    secondary_symbol='minus'
)

# Document pages

icon_document_page_disable = Icon(
    driver_name='fontawesomecss', css_classes='far fa-eye-slash'
)
icon_document_page_enable = Icon(
    driver_name='fontawesomecss', css_classes='far fa-eye'
)
icon_document_page_navigation_first = Icon(
    driver_name='fontawesome', symbol='step-backward'
)
icon_document_page_navigation_last = Icon(
    driver_name='fontawesome', symbol='step-forward'
)
icon_document_page_navigation_next = Icon(
    driver_name='fontawesome', symbol='arrow-right'
)
icon_document_page_navigation_previous = Icon(
    driver_name='fontawesome', symbol='arrow-left'
)
icon_document_page_return = icon_document
icon_document_page_rotate_left = Icon(
    driver_name='fontawesome', symbol='undo'
)
icon_document_page_rotate_right = Icon(
    driver_name='fontawesome', symbol='redo'
)
icon_document_page_view = Icon(
    driver_name='fontawesome', symbol='image'
)
icon_document_page_view_reset = Icon(
    driver_name='fontawesome', symbol='sync'
)
icon_document_page_zoom_in = Icon(
    driver_name='fontawesome', symbol='search-plus'
)
icon_document_page_zoom_out = Icon(
    driver_name='fontawesome', symbol='search-minus'
)
icon_document_pages = Icon(driver_name='fontawesome', symbol='copy')


icon_document_type_create = Icon(driver_name='fontawesome', symbol='plus')
icon_document_type_delete = Icon(driver_name='fontawesome', symbol='times')
icon_document_type_edit = Icon(driver_name='fontawesome', symbol='pencil-alt')
icon_document_type_filename = Icon(
    driver_name='fontawesome', symbol='keyboard'
)
icon_document_type_filename_create = Icon(
    driver_name='fontawesome', symbol='plus'
)
icon_document_type_policies = Icon(driver_name='fontawesome', symbol='times')
icon_document_type_setup = icon_document_type


icon_document_version_download = Icon(
    driver_name='fontawesome', symbol='download'
)
icon_document_version_list = Icon(
    driver_name='fontawesome', symbol='code-branch'
)
icon_document_version_return_document = icon_document
icon_document_version_return_list = Icon(
    driver_name='fontawesome', symbol='code-branch'
)
icon_document_version_view = Icon(
    driver_name='fontawesome', symbol='eye'
)
icon_document_version_revert = Icon(
    driver_name='fontawesome', symbol='undo'
)

icon_duplicated_document_list = Icon(
    driver_name='fontawesome', symbol='clone'
)
icon_duplicated_document_scan = Icon(
    driver_name='fontawesome', symbol='clone'
)

icon_recent_added_document_list = Icon(
    driver_name='fontawesome', symbol='asterisk'
)


icon_trash_can_empty = Icon(
    driver_name='fontawesome', symbol='trash-alt'
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
