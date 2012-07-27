from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from documents.statistics import get_statistics as documents_statistics
from ocr.statistics import get_statistics as ocr_statistics


def statistics_view(request):
    if request.user.is_superuser or request.user.is_staff:
        blocks = []
        blocks.append(documents_statistics())
        blocks.append(ocr_statistics())

        return render_to_response('statistics.html', {
            'blocks': blocks,
            'title': _(u'Statistics')
        },
        context_instance=RequestContext(request))
    else:
        raise PermissionDenied
