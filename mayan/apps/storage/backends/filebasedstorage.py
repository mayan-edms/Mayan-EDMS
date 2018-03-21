from __future__ import unicode_literals

import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .literals import DEFAULT_PATH


class FileBasedStorage(FileSystemStorage):
    """Simple wrapper for the stock Django FileSystemStorage class"""

    separator = os.path.sep

    def __init__(self, *args, **kwargs):
        self.location = kwargs.pop(
            'location', os.path.join(settings.MEDIA_ROOT, DEFAULT_PATH)
        )
        super(FileBasedStorage, self).__init__(*args, **kwargs)
