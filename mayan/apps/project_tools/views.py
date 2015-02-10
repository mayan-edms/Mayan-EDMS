from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .api import tool_items


def tools_list(request):
    context = {
        'object_navigation_links': tool_items,
        'title': _('Tools'),
    }

    return render_to_response('main/generic_list_horizontal.html', context,
                              context_instance=RequestContext(request))
