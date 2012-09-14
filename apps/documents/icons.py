from __future__ import absolute_import

from icons.literals import (LAYOUT, MAGNIFIER, PAGE, PAGE_COPY, PAGE_GEAR, PAGE_DELETE,
    PAGE_EDIT, PAGE_REFRESH, PAGE_SAVE, PAGE_WHITE_COPY, PAGE_WORLD, PRINTER,
    TABLE_RELATIONSHIP, PAGE_GO, PAGE_WHITE_CSHARP, CAMERA_DELETE, PAGE_WHITE_PICTURE,
    PAGE_WHITE_TEXT, PAGE_WHITE_EDIT, RESULTSET_NEXT, RESULTSET_PREVIOUS,
    RESULTSET_FIRST, RESULTSET_LAST, ZOOM_IN, ZOOM_OUT, ARROW_TURN_RIGHT,
    ARROW_TURN_LEFT, PAGE_WHITE, LAYOUT_EDIT, LAYOUT_ADD, LAYOUT_DELETE,
    DATABASE, DATABASE_ADD, DATABASE_EDIT, DATABASE_DELETE, PAGE_FIND)
from icons import Icon

icon_documents = Icon(PAGE)
icon_create_siblings = Icon(PAGE_COPY)
icon_document_properties = Icon(PAGE_GEAR)
icon_document_delete = Icon(PAGE_DELETE)
icon_document_edit = Icon(PAGE_EDIT)
icon_document_preview = Icon(MAGNIFIER)
icon_document_download = Icon(PAGE_SAVE)
icon_find_duplicates = Icon(PAGE_WHITE_COPY)
icon_print = Icon(PRINTER)
icon_version_revert = Icon(PAGE_REFRESH)
icon_version_compare = Icon(TABLE_RELATIONSHIP)
icon_versions = Icon(PAGE_WORLD)
icon_document_types = Icon(LAYOUT)
icon_document_type_document_list = Icon(PAGE_GO)
icon_document_update_page_count = Icon(PAGE_WHITE_CSHARP)
icon_document_clear_image_cache = Icon(CAMERA_DELETE)
icon_document_missing_list = Icon(PAGE_FIND)

icon_document_page_view = Icon(PAGE_WHITE_PICTURE)
icon_document_page_text = Icon(PAGE_WHITE_TEXT)
icon_document_page_edit = Icon(PAGE_WHITE_EDIT)
icon_document_page_navigation_next = Icon(RESULTSET_NEXT)
icon=icon_document_page_navigation_previous = Icon(RESULTSET_PREVIOUS)
icon_document_page_navigation_first = Icon(RESULTSET_FIRST)
icon_document_page_navigation_last = Icon(RESULTSET_LAST)
icon_document_page_zoom_in = Icon(ZOOM_IN)
icon_document_page_zoom_out = Icon(ZOOM_OUT)
icon_document_page_rotate_right = Icon(ARROW_TURN_RIGHT)
icon_document_page_rotate_left = Icon(ARROW_TURN_LEFT)
icon_document_page_view_reset = Icon(PAGE_WHITE)

icon_document_type_edit = Icon(LAYOUT_EDIT)
icon_document_type_delete = Icon(LAYOUT_DELETE)
icon_document_type_create = Icon(LAYOUT_ADD)

icon_document_type_filename_list = Icon(DATABASE)
icon_document_type_filename_create = Icon(DATABASE_ADD)
icon_document_type_filename_edit = Icon(DATABASE_EDIT)
icon_document_type_filename_delete = Icon(DATABASE_DELETE)
