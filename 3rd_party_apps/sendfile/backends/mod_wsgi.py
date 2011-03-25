from django.http import HttpResponse

from django.conf import settings
import os.path

def _convert_file_to_url(filename):
    # CURRENTLY NOT WORKING
    # mod_wsgi wants a relative URL not a filename
    # so apache does an internal redirect

    relpath = os.path.relpath(filename, settings.SENDFILE_ROOT)
    
    url = [settings.SENDFILE_URL]

    while relpath:
        relpath, head = os.path.split(relpath)
        url.insert(1, head)

    return u''.join(url)

def sendfile(request, filename, **kwargs):
    response = HttpResponse()
    response['Location'] = _convert_file_to_url(filename)
    # need to destroy get_host() to stop django
    # rewriting our location to include http, so that
    # mod_wsgi is able to do the internal redirect
    request.get_host = lambda: ''

    return response

