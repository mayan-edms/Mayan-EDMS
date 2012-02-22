from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from .forms import FeedbackForm
from .api import submit_form


def form_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                submit_form(form)
                messages.success(request, _(u'Thank you for submiting your feedback.'))
                return HttpResponseRedirect('/')
            except Exception, e:
                messages.error(request, _(u'Error submiting form; %s.') % e)
    else:
        form = FeedbackForm()

    return render_to_response('generic_form.html', {
        'title': _(u'feedback form'),
        'form': form,
    },
    context_instance=RequestContext(request))
