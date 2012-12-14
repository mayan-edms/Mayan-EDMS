from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

from .forms import RegistrationForm
from .models import RegistrationSingleton
from .exceptions import AlreadyRegistered


def form_view(request):
    registration = RegistrationSingleton.objects.get()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                registration.register(form)
                messages.success(request, _(u'Thank you for registering.'))
                return HttpResponseRedirect('/')
            except AlreadyRegistered:
                messages.error(request, _(u'Your copy is already registered.'))
                return HttpResponseRedirect('/')
            except Exception, e:
                messages.error(request, _(u'Error submiting form; %s.') % e)
    else:
        form = RegistrationForm()

    return render_to_response('generic_form.html', {
        'title': _(u'registration form'),
        'form': form,
    },
    context_instance=RequestContext(request))
