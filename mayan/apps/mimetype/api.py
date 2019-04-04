from __future__ import unicode_literals

import magic

from .settings import setting_file_read_size


def get_mimetype(file_object, mimetype_only=False):
    """
    Determine a file's mimetype by calling the system's libmagic
    library via python-magic.
    """
    file_mimetype = None
    file_mime_encoding = None

    read_size = setting_file_read_size.value
    if read_size == 0:
        # If the setting value is 0 that means disable read limit. To disable
        # the read limit passing None won't work, we pass -1 instead as per
        # the Python documentation.
        # https://docs.python.org/2/tutorial/inputoutput.html#methods-of-file-objects
        read_size = -1

    mime = magic.Magic(mime=True)
    file_mimetype = mime.from_buffer(file_object.read(read_size))
    file_object.seek(0)

    if not mimetype_only:
        file_object.seek(0)
        mime_encoding = magic.Magic(mime_encoding=True)
        file_mime_encoding = mime_encoding.from_buffer(file_object.read(read_size))
        file_object.seek(0)

    return file_mimetype, file_mime_encoding
