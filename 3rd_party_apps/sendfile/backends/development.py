from django.views.static import serve

import os.path

def sendfile(request, filename, **kwargs):
    '''
    Send file using django dev static file server.

    DO NOT USE IN PRODUCTION
    this is only to be used when developing and is provided
    for convenience only
    '''
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    return serve(request, basename, dirname)
