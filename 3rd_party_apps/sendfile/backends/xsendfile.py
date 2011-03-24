from django.http import HttpResponse

def sendfile(request, filename):
    response = HttpResponse()
    response['X-Sendfile'] = filename

    return response

