from __future__ import absolute_import

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from .models import App


def app_list(request):
    #order =  [i for i,f in sorted(smart_modules.items(), key=lambda k: 'dependencies' in k[1] and k[1]['dependencies'])]

    return render_to_response('generic_list.html', {
        'object_list' : App.live.all(),
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'name'), 'attribute': 'name'},
            {'name': _(u'label'), 'attribute': 'label'},
        ],
    }, context_instance=RequestContext(request))
