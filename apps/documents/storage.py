from django.core.files.storage import FileSystemStorage

class DocumentStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super(DocumentStorage, self).__init__(*args, **kwargs)
        self.location='document_storage'

