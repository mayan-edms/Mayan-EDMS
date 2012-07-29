from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from .api import statistics_functions


def statistics_view(request):
    if request.user.is_superuser or request.user.is_staff:
        blocks = [function() for function in statistics_functions]

        return render_to_response('statistics.html', {
            'blocks': blocks,
            'title': _(u'Statistics')
        },
        context_instance=RequestContext(request))
    else:
        raise PermissionDenied
