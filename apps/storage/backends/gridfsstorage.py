from __future__ import absolute_import

import os

from django.core.files.storage import Storage
from django.utils.encoding import force_unicode

from pymongo import Connection
from gridfs import GridFS

from storage import settings


class GridFSStorage(Storage):
    separator = u'/'

    def __init__(self, *args, **kwargs):
        self.db = Connection(host=settings.GRIDFS_HOST,
            port=settings.GRIDFS_PORT)[settings.GRIDFS_DATABASE_NAME]
        self.fs = GridFS(self.db)

    def save(self, name, content):
        #TODO: if exists add _ plus a counter
        while True:
            try:
                # This file has a file path that we can move.
                if hasattr(content, 'temporary_file_path'):
                    self.move(content.temporary_file_path(), name)
                    content.close()
                # This is a normal uploadedfile that we can stream.
                else:
                    # This fun binary flag incantation makes os.open throw an
                    # OSError if the file already exists before we open it.
                    newfile = self.fs.new_file(filename=name)
                    try:
                        for chunk in content.chunks():
                            newfile.write(chunk)
                    finally:
                        newfile.close()
            except Exception, e:  # OSError, e:
            #    if e.errno == errno.EEXIST:
            #        # Ooops, the file exists. We need a new file name.
            #        name = self.get_available_name(name)
            #        full_path = self.path(name)
            #    else:
            #        raise
                raise
            else:
                # OK, the file save worked. Break out of the loop.
                break

        return name

    def open(self, name, *args, **kwars):
        return self.fs.get_last_version(name)

    def delete(self, name):
        oid = self.fs.get_last_version(name)._id
        self.fs.delete(oid)

    def exists(self, name):
        return self.fs.exists(filename=name)

    def path(self, name):
        return force_unicode(name)

    def size(self, name):
        return self.fs.get_last_version(name).length

    def move(self, old_file_name, name, chunk_size=1024 * 64):
        # first open the old file, so that it won't go away
        old_file = open(old_file_name, 'rb')
        try:
            newfile = self.fs.new_file(filename=name)

            try:
                current_chunk = None
                while current_chunk != '':
                    current_chunk = old_file.read(chunk_size)
                    newfile.write(current_chunk)
            finally:
                newfile.close()
        finally:
            old_file.close()

        try:
            os.remove(old_file_name)
        except OSError, e:
            # Certain operating systems (Cygwin and Windows)
            # fail when deleting opened files, ignore it.  (For the
            # systems where this happens, temporary files will be auto-deleted
            # on close anyway.)
            if getattr(e, 'winerror', 0) != 32 and getattr(e, 'errno', 0) != 13:
                raise
