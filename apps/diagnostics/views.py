from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .api import diagnostics


def diagnostics_view(request):
    return render_to_response('diagnostics.html', {
        'blocks': diagnostics,
        'title': _(u'Diagnostics')
    },
    context_instance=RequestContext(request))
