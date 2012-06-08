from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from navigation.widgets import button_navigation_widget

from . import setup_menu


def setup_list(request):
    context = {
        'object_list': [button_navigation_widget(request, item.get('link')) for item in setup_menu.getchildren()],
        'title': _(u'setup items'),
    }

    # Remove unresolved links form list
    context['object_list'] = [obj for obj in context['object_list'] if obj]

    return render_to_response('generic_list_horizontal.html', context,
        context_instance=RequestContext(request))
