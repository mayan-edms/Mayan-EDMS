from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.importlib import import_module

from converter.conf.settings import GRAPHICS_BACKEND


def _lazy_load(fn):
    _cached = []

    def _decorated():
        if not _cached:
            _cached.append(fn())
        return _cached[0]
    return _decorated


@_lazy_load
def _get_backend():
    return import_module(GRAPHICS_BACKEND)

try:
    backend = _get_backend()
except ImportError:
    raise ImportError(u'Missing or incorrect converter backend: %s' % GRAPHICS_BACKEND)


def formats_list(request):
    #check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    context = {
        'title': _(u'suported file formats'),
        'hide_object': True,
        'object_list': backend.get_format_list(),
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': lambda x: x[0]
            },
            {
                'name': _(u'description'),
                'attribute': lambda x: x[1]
            }
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
