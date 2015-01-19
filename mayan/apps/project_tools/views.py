from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from navigation.widgets import button_navigation_widget

from .api import tool_items


def tools_list(request):
    context = {
        'object_list': [button_navigation_widget(request, item) for item in tool_items],
        'title': _('Tools'),
    }

    return render_to_response('main/generic_list_horizontal.html', context,
        context_instance=RequestContext(request))
