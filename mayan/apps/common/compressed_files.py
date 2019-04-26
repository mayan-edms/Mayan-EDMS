from __future__ import unicode_literals

from io import BytesIO
import tarfile
import zipfile

try:
    import zlib  # NOQA
    COMPRESSION = zipfile.ZIP_DEFLATED
except ImportError:
    COMPRESSION = zipfile.ZIP_STORED

from django.core.files.uploadedfile import SimpleUploadedFile

from mayan.apps.mimetype.api import get_mimetype

from .exceptions import NoMIMETypeMatch


class Archive(object):
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
        # Remove the zinfo_or_arcname and bytes keyword arguments
        # so that the writestr methods works on Python 2 and 3
        # Python 2 syntax:
        # ZipFile.writestr(zinfo_or_arcname, bytes[, compress_type])
        # Python 3 syntax:
        # ZipFile.writestr(
        #    zinfo_or_arcname, data, compress_type=None, compresslevel=None
        # )
        # TODO: Change this to keyword arguments when the move to Python 3
        # and Django 2.x is complete.
        self._archive.writestr(
            filename, file_object.read(), compress_type=COMPRESSION
        )

    def create(self):
        self.string_buffer = BytesIO()
        self._archive = zipfile.ZipFile(self.string_buffer, mode='w')

    def member_contents(self, filename):
        return self._archive.read(filename)

    def members(self):
        return [
            filename for filename in self._archive.namelist() if not filename.endswith('/')
        ]

    def open_member(self, filename):
        return self._archive.open(filename)

    def write(self, filename=None):
        # fix for Linux zip files read in Windows
        for entry in self._archive.filelist:
            entry.create_system = 0

        self.string_buffer.seek(0)

        if filename:
            with open(filename, 'w') as file_object:
                file_object.write(self.string_buffer.read())
        else:
            return self.string_buffer

    def as_file(self, filename):
        return SimpleUploadedFile(name=filename, content=self.write().read())


Archive.register(
    archive_classes=(ZipArchive,), mime_types=('application/zip',)
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
