VERSION = (0, 1, 1)
__version__ = '.'.join(map(str, VERSION))

import os.path
from mimetypes import guess_type

from django.http import Http404

def _lazy_load(fn):
    _cached = []
    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]
    return _decorated


@_lazy_load
def _get_sendfile():
    from django.utils.importlib import import_module
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured

    backend = getattr(settings, 'SENDFILE_BACKEND', None)
    if not backend:
        raise ImproperlyConfigured('You must specify a valued for SENDFILE_BACKEND')
    module = import_module(backend)
    return module.sendfile



def sendfile(request, filename, attachment=False, attachment_filename=None):
    '''
    create a response to send file using backend configured in SENDFILE_BACKEND

    if attachment is True the content-disposition header will be set with either
    the filename given or else the attachment_filename (of specified).  This
    will typically prompt the user to download the file, rather than view it.
    '''
    _sendfile = _get_sendfile()

    if not os.path.exists(filename):
        raise Http404('"%s" does not exist' % filename)

    mimetype, encoding = guess_type(filename)
    if mimetype is None:
        mimetype = 'application/octet-stream'
        
    response = _sendfile(request, filename, mimetype=mimetype)
    if attachment:
        attachment_filename = attachment_filename or os.path.basename(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % attachment_filename

    response['Content-length'] = os.path.getsize(filename)
    response['Content-Type'] = mimetype
    if encoding:
        response['Content-Encoding'] = encoding

    return response
