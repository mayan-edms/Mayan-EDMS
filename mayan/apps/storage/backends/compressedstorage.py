from __future__ import unicode_literals

import zipfile

try:
    import zlib  # NOQA
    COMPRESSION = zipfile.ZIP_DEFLATED
except ImportError:
    COMPRESSION = zipfile.ZIP_STORED

from django.core.files.base import ContentFile
from django.utils.encoding import force_text

from ..classes import BufferedFile, PassthroughStorage

from .literals import ZIP_CHUNK_SIZE, ZIP_MEMBER_FILENAME


class BufferedZipFile(BufferedFile):
    def __init__(self, *args, **kwargs):
        self.member_name = kwargs.pop('member_name')
        super(BufferedZipFile, self).__init__(*args, **kwargs)
        self.binary_mode = 'b' in self.mode
        self.zip_container_file_object = zipfile.ZipFile(
            file=self.file_object
        )
        self.zip_file_object = self.zip_container_file_object.open(
            name=self.member_name
        )

    def close(self):
        self.zip_file_object.close()
        self.zip_container_file_object.close()
        self.file_object.close()

    def _get_file_object_chunk(self):
        chunk = self.zip_file_object.read(ZIP_CHUNK_SIZE)

        if chunk:
            if self.binary_mode:
                return chunk
            else:
                return force_text(chunk)


class ZipCompressedPassthroughStorage(PassthroughStorage):
    def open(self, name, mode='rb', _direct=False):
        upstream_kwargs = {'name': name}
        if _direct:
            upstream_kwargs['mode'] = mode

            if issubclass(self.upstream_storage_class, PassthroughStorage):
                upstream_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='open', kwargs=upstream_kwargs
            )
        else:
            # Mode is always 'rb' when reading the zip file
            upstream_kwargs['mode'] = 'rb'
            storage_file = self._call_backend_method(
                method_name='open', kwargs=upstream_kwargs
            )
            return BufferedZipFile(
                file_object=storage_file, member_name=ZIP_MEMBER_FILENAME,
                mode=mode
            )

    def save(self, name, content, max_length=None, _direct=False):
        upstream_kwargs = {'max_length': max_length, 'name': name}
        if _direct:
            upstream_kwargs['content'] = content

            if issubclass(self.upstream_storage_class, PassthroughStorage):
                upstream_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='save', kwargs=upstream_kwargs
            )
        else:
            name = self._call_backend_method(
                method_name='save', kwargs={
                    'content': ContentFile(content=''), 'name': name
                }
            )
            with self._call_backend_method(
                method_name='open', kwargs={
                    'name': name, 'mode': 'wb'
                }
            ) as file_object:
                with zipfile.ZipFile(file=file_object, mode='w', compression=COMPRESSION) as zip_file_object:
                    zip_file_object.writestr(ZIP_MEMBER_FILENAME, content.read())

                    for file in zip_file_object.filelist:
                        file.create_system = 0

            return name
