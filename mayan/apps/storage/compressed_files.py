from io import BytesIO
import tarfile
import zipfile

import extract_msg

try:
    import zlib  # NOQA
    COMPRESSION = zipfile.ZIP_DEFLATED
except ImportError:
    COMPRESSION = zipfile.ZIP_STORED

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.encoding import force_bytes, force_text

from mayan.apps.mimetype.api import get_mimetype

from .exceptions import NoMIMETypeMatch
from .literals import MSG_MIME_TYPES


class Archive:
    _registry = {}

    @classmethod
    def register(cls, mime_types, archive_classes):
        for mime_type in mime_types:
            for archive_class in archive_classes:
                cls._registry.setdefault(
                    mime_type, []
                ).append(archive_class)

    @classmethod
    def open(cls, file_object):
        mime_type = get_mimetype(
            file_object=file_object, mimetype_only=True
        )[0]

        try:
            for archive_class in cls._registry[mime_type]:
                instance = archive_class()
                instance._open(file_object=file_object)
                return instance
        except KeyError:
            raise NoMIMETypeMatch

    def _open(self, file_object):
        raise NotImplementedError

    def add_file(self, file_object, filename):
        """
        Add a file as a member of an archive
        """
        raise NotImplementedError

    def close(self):
        self._archive.close()

    def create(self):
        """
        Create an empty archive
        """
        raise NotImplementedError

    def get_members(self):
        return (
            SimpleUploadedFile(
                content=self.member_contents(filename=filename), name=filename
            ) for filename in self.members()
        )

    def member_contents(self, filename):
        """
        Return the content of a member
        """
        raise NotImplementedError

    def members(self):
        """
        Return a list of all the elements inside the archive
        """
        raise NotImplementedError

    def open_member(self, filename):
        """
        Return a file-like object to a member of the archive
        """
        raise NotImplementedError


class MsgArchive(Archive):
    def _open(self, file_object):
        self._archive = extract_msg.Message(file_object)

    def member_contents(self, filename):
        if filename == 'message.txt':
            return force_bytes(s=self._archive.body)

        for member in self._archive.attachments:
            if member.longFilename == filename:
                return force_bytes(s=member.data)

    def members(self):
        results = []
        for attachments in self._archive.attachments:
            results.append(attachments.longFilename)

        if self._archive.body:
            results.append('message.txt')

        return results

    def open_member(self, filename):
        if filename == 'message.txt':
            return BytesIO(force_bytes(s=self._archive.body))

        for member in self._archive.attachments:
            if member.longFilename == filename:
                return BytesIO(force_bytes(s=member.data))


class TarArchive(Archive):
    def _open(self, file_object):
        self._archive = tarfile.open(fileobj=file_object)

    def add_file(self, file_object, filename):
        self._archive.addfile(
            tarfile.TarInfo(), fileobj=file_object
        )

    def create(self):
        self.string_buffer = BytesIO()
        self._archive = tarfile.TarFile(fileobj=self.string_buffer, mode='w')

    def member_contents(self, filename):
        return self._archive.extractfile(filename).read()

    def members(self):
        return self._archive.getnames()

    def open_member(self, filename):
        return self._archive.extractfile(filename)


class ZipArchive(Archive):
    def _open(self, file_object):
        self._archive = zipfile.ZipFile(file_object)

    def add_file(self, file_object, filename):
        self._archive.writestr(
            filename, file_object.read(), compress_type=COMPRESSION
        )

    def create(self):
        self.string_buffer = BytesIO()
        self._archive = zipfile.ZipFile(self.string_buffer, mode='w')

    def member_contents(self, filename):
        return self._archive.read(filename)

    def members(self):
        results = []

        for filename in self._archive.namelist():
            # Zip files only support UTF-8 and CP437 encodings.
            # Attempt to decode CP437 to be able to check if it ends
            # with a slash.
            # Future improvement that violates the Zip format:
            # Add chardet.detect to detect the most likely encoding
            # if other than CP437.
            try:
                filename = filename.decode('CP437')
                is_unicode = False
            except AttributeError:
                filename = force_text(s=filename)
                is_unicode = True
            except UnicodeEncodeError:
                is_unicode = True

            if not filename.endswith('/'):
                # Re encode in the original encoding
                if not is_unicode:
                    filename = filename.encode(
                        encoding='CP437', errors='strict'
                    )

                results.append(filename)

        return results

    def open_member(self, filename):
        return self._archive.open(filename)

    def write(self, filename=None):
        # fix for Linux zip files read in Windows
        for entry in self._archive.filelist:
            entry.create_system = 0

        self.string_buffer.seek(0)

        if filename:
            with open(file=filename, mode='w') as file_object:
                file_object.write(self.string_buffer.read())
        else:
            return self.string_buffer

    def as_file(self, filename):
        return SimpleUploadedFile(name=filename, content=self.write().read())


Archive.register(
    archive_classes=(MsgArchive,), mime_types=MSG_MIME_TYPES
)
Archive.register(
    archive_classes=(TarArchive,), mime_types=('application/x-tar',)
)
Archive.register(
    archive_classes=(TarArchive,), mime_types=('application/gzip',)
)
Archive.register(
    archive_classes=(TarArchive,), mime_types=('application/x-bzip2',)
)
Archive.register(
    archive_classes=(ZipArchive,), mime_types=('application/zip',)
)
