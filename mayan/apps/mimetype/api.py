from __future__ import unicode_literals

import os

try:
    import magic
    USE_PYTHON_MAGIC = True
except:
    import mimetypes
    mimetypes.init()
    USE_PYTHON_MAGIC = False


def get_mimetype(file_description, filepath, mimetype_only=False):
    """
    Determine a file's mimetype by calling the system's libmagic
    library via python-magic or fallback to use python's mimetypes
    library
    """
    file_mimetype = None
    file_mime_encoding = None
    if USE_PYTHON_MAGIC:
        mime = magic.Magic(mime=True)
        file_mimetype = mime.from_buffer(file_description.read())
        if not mimetype_only:
            file_description.seek(0)
            mime_encoding = magic.Magic(mime_encoding=True)
            file_mime_encoding = mime_encoding.from_buffer(file_description.read())
    else:
        path, filename = os.path.split(filepath)
        file_mimetype, file_mime_encoding = mimetypes.guess_type(filename)

    file_description.close()

    return file_mimetype, file_mime_encoding
