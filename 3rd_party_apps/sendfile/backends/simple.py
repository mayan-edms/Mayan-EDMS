from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

def sendfile(request, filename):
    wrapper = FileWrapper(file(filename))
    return HttpResponse(wrapper)
