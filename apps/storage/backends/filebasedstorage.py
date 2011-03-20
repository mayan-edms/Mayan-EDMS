import os

from django.core.files.storage import FileSystemStorage

from storage.conf.settings import FILESTORAGE_LOCATION

class FileBasedStorage(FileSystemStorage):
    separator = os.path.sep
    
    def __init__(self, *args, **kwargs):
        super(FileBasedStorage, self).__init__(*args, **kwargs)
        self.location=FILESTORAGE_LOCATION

