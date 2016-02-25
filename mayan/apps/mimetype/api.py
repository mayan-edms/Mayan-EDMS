from __future__ import unicode_literals

import magic


def get_mimetype(file_object, mimetype_only=False):
    """
    Determine a file's mimetype by calling the system's libmagic
    library via python-magic or fallback to use python's mimetypes
    library
    """
    file_mimetype = None
    file_mime_encoding = None

    mime = magic.Magic(mime=True)
    file_mimetype = mime.from_buffer(file_object.read())
    file_object.seek(0)

    if not mimetype_only:
        file_object.seek(0)
        mime_encoding = magic.Magic(mime_encoding=True)
        file_mime_encoding = mime_encoding.from_buffer(file_object.read())
        file_object.seek(0)

    # Special case for PCL files
    if file_mimetype in ('application/octet-stream', 'text/plain'):
        signature = file_object.read(2)
        file_object.seek(0)
        # Two-Character Escape Sequences ASCII 48-126
        # Parameterized Escape Sequences ASCII 33-47
        if signature[0] == b'\x1b' and ord(signature[1]) >= 33 and ord(signature[1]) <= 126:
            file_mimetype = 'application/x-pcl'

    return file_mimetype, file_mime_encoding
