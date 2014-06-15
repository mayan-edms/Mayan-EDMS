import zipfile

try:
    import zlib
    COMPRESSION = zipfile.ZIP_DEFLATED
except:
    COMPRESSION = zipfile.ZIP_STORED

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.files.uploadedfile import SimpleUploadedFile


class NotACompressedFile(Exception):
    pass


class CompressedFile(object):
    def __init__(self, file_input=None):
        if file_input:
            self._open(file_input)
        else:
            self._create()

    def _create(self):
        self.descriptor = StringIO()
        self.zf = zipfile.ZipFile(self.descriptor, mode='w')

    def _open(self, file_input):
        try:
            # Is it a file like object?
            file_input.seek(0)
        except AttributeError:
            # If not, try open it.
            self.descriptor = open(file_input, 'r+b')
        else:
            self.descriptor = file_input

        try:
            test = zipfile.ZipFile(self.descriptor, mode='r')
        except zipfile.BadZipfile:
            raise NotACompressedFile
        else:
            test.close()
            self.descriptor.seek(0)
            self.zf = zipfile.ZipFile(self.descriptor, mode='a')

    def add_file(self, file_input, arcname=None):
        try:
            # Is it a file like object?
            file_input.seek(0)
        except AttributeError:
            # If not, keep it
            self.zf.write(file_input, arcname=arcname, compress_type=COMPRESSION)
        else:
            self.zf.writestr(arcname, file_input.read())

    def contents(self):
        return [filename for filename in self.zf.namelist() if not filename.endswith('/')]

    def get_content(self, filename):
        return self.zf.read(filename)

    def write(self, filename=None):
        # fix for Linux zip files read in Windows
        for file in self.zf.filelist:
            file.create_system = 0

        self.descriptor.seek(0)

        if filename:
            descriptor = open(filename, 'w')
            descriptor.write(self.descriptor.read())
        else:
            return self.descriptor

    def as_file(self, filename):
        return SimpleUploadedFile(name=filename, content=self.write().read())

    def close(self):
        self.zf.close()
