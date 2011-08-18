from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from project_setup.api import setup_items
from project_setup.widgets import setup_button_widget


def setup_list(request):
    context = {
        'object_list': [setup_button_widget(request, item) for item in setup_items],
        'title': _(u'setup items'),
    }

    return render_to_response('generic_list_horizontal.html', context,
        context_instance=RequestContext(request))
