from __future__ import absolute_import

import os

from django.core.files.storage import FileSystemStorage

from storage.settings import FILESTORAGE_LOCATION


class FileBasedStorage(FileSystemStorage):
    """
    Simple wrapper for the stock Django FileSystemStorage class
    """
    separator = os.path.sep

    def __init__(self, *args, **kwargs):
        super(FileBasedStorage, self).__init__(*args, **kwargs)
        self.location = FILESTORAGE_LOCATION
