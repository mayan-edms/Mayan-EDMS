from __future__ import absolute_import

from icons.literals import (DOCUMENT_SIGNATURE, KEY, KEY_DELETE, KEY_ADD,
    ZOOM, LIGHTNING, CROSS, USER_SILHOUETTE)
from icons import Icon

icon_private_keys = Icon(KEY)
icon_public_keys = Icon(KEY)
icon_key_delete = Icon(KEY_DELETE)
icon_key_query = Icon(ZOOM)
icon_key_receive = Icon(KEY_ADD)
icon_key_setup = Icon(KEY)
icon_document_signature = Icon(DOCUMENT_SIGNATURE)

icon_bad_signature = Icon(CROSS)
icon_no_signature = Icon(CROSS)
icon_signature_error = Icon(CROSS)
icon_no_public_key = Icon(USER_SILHOUETTE)
icon_good_signature = Icon(DOCUMENT_SIGNATURE)
icon_valid_signature = Icon(DOCUMENT_SIGNATURE)
