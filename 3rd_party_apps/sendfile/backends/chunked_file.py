from django.http import HttpResponse
from django.core.files.uploadedfile import SimpleUploadedFile

def sendfile(request, filename):
    return = HttpResponse(IterFile(filename))

class IterFile(object):
    def __init__(self, filename):
        self.file = SimpleUploadedFile(name=filename, content=open(filename).read())

    def __iter__(self):
        return self.file.chunks()

