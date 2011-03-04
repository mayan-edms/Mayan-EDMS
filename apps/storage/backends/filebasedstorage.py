from django.core.files.storage import FileSystemStorage

class FileBasedStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super(FileBasedStorage, self).__init__(*args, **kwargs)
        self.location='document_storage'

