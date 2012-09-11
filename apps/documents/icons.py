from __future__ import absolute_import

from icons.literals import (LAYOUT, MAGNIFIER, PAGE, PAGE_COPY, PAGE_GEAR, PAGE_DELETE,
    PAGE_EDIT, PAGE_REFRESH, PAGE_SAVE, PAGE_WHITE_COPY, PAGE_WORLD, PRINTER,
    TABLE_RELATIONSHIP)
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
