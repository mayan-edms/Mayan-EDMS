from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied

from common.utils import encapsulate

from .api import get_format_list
from .settings import GRAPHICS_BACKEND


def formats_list(request):
    if request.user.is_superuser or request.user.is_staff:
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
    else:
        raise PermissionDenied
