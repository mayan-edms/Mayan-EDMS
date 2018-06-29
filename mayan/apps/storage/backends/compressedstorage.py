from __future__ import unicode_literals

import os
import zipfile

try:
    import zlib  # NOQA
    COMPRESSION = zipfile.ZIP_DEFLATED
except ImportError:
    COMPRESSION = zipfile.ZIP_STORED

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.files import File
from django.core.files.storage import FileSystemStorage


class CompressedStorage(FileSystemStorage):
    """Simple wrapper for the stock Django FileSystemStorage class"""

    separator = os.path.sep

    def __init__(self, *args, **kwargs):
        self.location = kwargs.pop('location')
        super(CompressedStorage, self).__init__(*args, **kwargs)

    def save(self, name, content):
        descriptor = StringIO()
        zf = zipfile.ZipFile(descriptor, mode='w', compression=COMPRESSION)

        zf.writestr('document', content.read())

        for file in zf.filelist:
            file.create_system = 0

        zf.close()
        descriptor.seek(0)
        return super(CompressedStorage, self).save(name, File(descriptor))

    def open(self, name, mode='rb'):
        storage_file = super(CompressedStorage, self).open(name, mode)
        zf = zipfile.ZipFile(storage_file)
        descriptor = StringIO()
        descriptor.write(zf.read('document'))
        descriptor.seek(0)
        return File(descriptor)
