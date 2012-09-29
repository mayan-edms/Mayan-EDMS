from __future__ import absolute_import

from icons.literals import (XHTML, XHTML_GO, XHTML_ADD, XHTML_DELETE, XHTML_EDIT,
    TABLE, TABLE_ADD, TABLE_EDIT, TABLE_DELETE, TABLE_REFRESH)
from icons import Icon

icon_metadata_view = Icon(XHTML)
icon_metadata_edit = Icon(XHTML_EDIT)
icon_metadata_add = Icon(XHTML_ADD)
icon_metadata_remove = Icon(XHTML_DELETE)

icon_metadata_sets = Icon(TABLE)
icon_metadata_set_create = Icon(TABLE_ADD)
icon_metadata_set_edit = Icon(TABLE_EDIT)
icon_metadata_set_delete = Icon(TABLE_DELETE)
icon_metadata_set_members = Icon(TABLE_REFRESH)
