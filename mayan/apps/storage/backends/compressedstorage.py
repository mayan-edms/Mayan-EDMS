from __future__ import unicode_literals

import zipfile

try:
    import zlib  # NOQA
    COMPRESSION = zipfile.ZIP_DEFLATED
except ImportError:
    COMPRESSION = zipfile.ZIP_STORED

from django.utils.six import BytesIO, StringIO

from django.core.files.base import ContentFile
from django.utils.encoding import force_text

from ..classes import PassthroughStorage

MEMBER_FILENAME = 'mayan_file'


class ZipCompressedPassthroughStorage(PassthroughStorage):
    def open(self, name, mode='rb'):
        # Mode is always 'rb' when reading the zip file
        storage_file = self._call_backend_method(
            method_name='open', kwargs={'name': name, 'mode': 'rb'}
        )
        binary_mode = 'b' in mode

        if binary_mode:
            stream = BytesIO()
        else:
            stream = StringIO()

        with zipfile.ZipFile(file=storage_file) as file_object:
            data = file_object.read(name=MEMBER_FILENAME)
            if not binary_mode:
                data = force_text(data)

            stream.write(data)

            stream.seek(0)

        if binary_mode:
            return ContentFile(content=stream.getbuffer())
        else:
            return ContentFile(content=stream.getvalue())

    def save(self, name, content, max_length=None):
        stream = BytesIO()
        with zipfile.ZipFile(file=stream, mode='w', compression=COMPRESSION) as file_object:
            file_object.writestr(MEMBER_FILENAME, content.read())

            for file in file_object.filelist:
                file.create_system = 0

        stream.seek(0)
        return self._call_backend_method(
            method_name='save', kwargs={
                'content': ContentFile(content=stream.getbuffer()),
                'max_length': max_length, 'name': name
            }
        )
