import zipfile

from django.core.files.uploadedfile import SimpleUploadedFile


class NotACompressedFile(Exception):
    pass


class CompressedFile(object):
    def __init__(self, file_object):
        self.file_object = file_object

    def children(self):
        try:
            # Try for a ZIP file
            zfobj = zipfile.ZipFile(self.file_object)
            filenames = [filename for filename in zfobj.namelist() if not filename.endswith('/')]
            return (SimpleUploadedFile(name=filename, content=zfobj.read(filename)) for filename in filenames)
        except zipfile.BadZipfile:
            raise NotACompressedFile

    #def close(self):
    #    self.file_object.close()
