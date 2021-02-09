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
        super().__init__(*args, **kwargs)
        self.binary_mode = 'b' in self.mode

        if 'r' in self.mode:
            zip_mode = 'r'
        else:
            zip_mode = 'w'

        self.zip_container_file_object = zipfile.ZipFile(
            file=self.file_object, mode=zip_mode
        )
        self.zip_file_object = self.zip_container_file_object.open(
            name=self.member_name, mode=zip_mode
        )

    def _get_file_object_chunk(self):
        chunk = self.zip_file_object.read(ZIP_CHUNK_SIZE)

        if chunk:
            if self.binary_mode:
                return chunk
            else:
                return force_text(s=chunk)

    def close(self):
        self.zip_file_object.close()
        self.zip_container_file_object.close()
        self.file_object.close()

    def tell(self):
        return self.zip_file_object.tell()

    def write(self, data):
        return self.zip_file_object.write(data)


class ZipCompressedPassthroughStorage(PassthroughStorage):
    def open(self, name, mode='rb', _direct=False):
        next_kwargs = {'name': name}

        if _direct:
            next_kwargs['mode'] = mode

            if issubclass(self.next_storage_class, PassthroughStorage):
                next_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='open', kwargs=next_kwargs
            )
        else:
            # Next storage mode is always 'rb+' when reading the zip file
            next_kwargs['mode'] = 'rb+'

            storage_file = self._call_backend_method(
                method_name='open', kwargs=next_kwargs
            )

            return BufferedZipFile(
                file_object=storage_file, member_name=ZIP_MEMBER_FILENAME,
                mode=mode
            )

    def save(self, name, content, max_length=None, _direct=False):
        next_kwargs = {'max_length': max_length, 'name': name}
        if _direct:
            next_kwargs['content'] = content

            if issubclass(self.next_storage_class, PassthroughStorage):
                next_kwargs.update({'_direct': _direct})

            return self._call_backend_method(
                method_name='save', kwargs=next_kwargs
            )
        else:
            if not self._call_backend_method(
                method_name='exists', kwargs={'name': name}
            ):
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
                # From Python: ZipFile requires mode 'r', 'w', 'x', or 'a'
                with zipfile.ZipFile(file=file_object, mode='w', compression=COMPRESSION) as zip_file_object:
                    zip_file_object.writestr(ZIP_MEMBER_FILENAME, content.read())

                    for file in zip_file_object.filelist:
                        file.create_system = 0

            return name
