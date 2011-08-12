from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.utils import encapsulate

from converter.api import get_format_list
from converter.conf.settings import GRAPHICS_BACKEND


def formats_list(request):
    #check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    context = {
        'title': _(u'suported file formats'),
        'hide_object': True,
        'object_list': sorted(get_format_list()),
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': encapsulate(lambda x: x[0])
            },
            {
                'name': _(u'description'),
                'attribute': encapsulate(lambda x: x[1])
            }
        ],
        'backend': GRAPHICS_BACKEND,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
