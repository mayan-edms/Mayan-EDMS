from __future__ import unicode_literals

import base64
import os
import urllib

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.files import File

from converter.api import convert
from mimetype.api import get_mimetype


class PseudoFile(File):
    def __init__(self, file, name):
        self.name = name
        self.file = file
        self.file.seek(0, os.SEEK_END)
        self.size = self.file.tell()
        self.file.seek(0)


class SourceUploadedFile(File):
    def __init__(self, source, file, extra_data=None):
        self.file = file
        self.source = source
        self.extra_data = extra_data


class Attachment(File):
    def __init__(self, part, name):
        self.name = name
        self.file = PseudoFile(StringIO(part.get_payload(decode=True)), name=name)


class StagingFile(object):
    """
    Simple class to extend the File class to add preview capabilities
    files in a directory on a storage
    """
    def __init__(self, staging_folder, filename=None, encoded_filename=None):
        self.staging_folder = staging_folder
        if encoded_filename:
            self.encoded_filename = str(encoded_filename)
            self.filename = base64.urlsafe_b64decode(urllib.unquote_plus(self.encoded_filename))
        else:
            self.filename = filename
            self.encoded_filename = base64.urlsafe_b64encode(filename)

    def __unicode__(self):
        return unicode(self.filename)

    def as_file(self):
        return File(file=open(self.get_full_path(), mode='rb'), name=self.filename)

    def get_full_path(self):
        return os.path.join(self.staging_folder.folder_path, self.filename)

    def get_image(self, size, page, zoom, rotation, as_base64=True):
        # TODO: add support for transformations
        converted_file_path = convert(self.get_full_path(), size=size)

        if as_base64:
            mimetype = get_mimetype(open(converted_file_path, 'r'), converted_file_path, mimetype_only=True)[0]
            image = open(converted_file_path, 'r')
            base64_data = base64.b64encode(image.read())
            image.close()
            return 'data:%s;base64,%s' % (mimetype, base64_data)
        else:
            return converted_file_path

    def delete(self):
        os.unlink(self.get_full_path())
