from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def home(request):
    return render_to_response('home.html', {},
        context_instance=RequestContext(request))
